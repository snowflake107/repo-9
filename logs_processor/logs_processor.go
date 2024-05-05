package logs_processor

import (
	"archive/zip"
	"bytes"
	"compress/gzip"
	"encoding/json"
	"fmt"
	"github.com/aws/aws-sdk-go/service/s3"
	"go.uber.org/zap"
	"io/ioutil"
	"strings"
)

const (
	fieldType      = "type"
	fieldMessage   = "message"
	fieldS3Key     = "s3_object_key"
	fieldAwsRegion = "aws_region"
	defaultLogType = "s3_hook"
)

func ProcessLogs(s3Object *s3.GetObjectOutput, logger *zap.Logger, key, bucket, awsRegion string) [][]byte {
	// Initializing variables
	var logsStr string
	buf := new(bytes.Buffer)

	// Read file
	_, err := buf.ReadFrom(s3Object.Body)
	if err != nil {
		logger.Error(fmt.Sprintf("Cannot proccess object %s. Error: %s", key, err.Error()))
		return nil
	}

	// Decompress if needed and extract logs from file
	logsStr = getBody(buf, logger)
	s3Logs := strings.Split(logsStr, "\n")
	keyLower := strings.ToLower(key)

	// Process logs in the detected format
	if strings.Contains(keyLower, cloudtrailName) {
		logger.Debug(fmt.Sprintf("Detected %s logs", cloudtrailName))
		return processCloudTrailLogs(s3Logs, logger, key, bucket, awsRegion)
	} else if strings.HasSuffix(keyLower, "json.gzip") || strings.HasSuffix(keyLower, "json.zip") || strings.HasSuffix(keyLower, "json") {
		logger.Debug("Detected Json logs.")
		return processJsonLogs(s3Logs, logger, key, bucket, awsRegion)
	}
	logger.Debug("Processing the logs as Text.")
	return processTxtLogs(s3Logs, logger, key, bucket, awsRegion)
}

func processCloudTrailLogs(s3Logs []string, logger *zap.Logger, key, bucket, awsRegion string) [][]byte {
	// Initializing variables
	logs := make([][]byte, 0)
	var logsJsons []map[string]interface{}

	// Process logs
	controlTowerParsing := getControlTowerParsing()
	for _, s3Log := range s3Logs {
		if len(s3Log) == 0 {
			continue
		}
		logsJsons = extractCloudtrailLogsFromFile(s3Log, logger)
		logs = addFieldsAndAppendLogsToFinalList(logs, logsJsons, logger, key, bucket, awsRegion, controlTowerParsing)
	}
	return logs
}

func processTxtLogs(s3Logs []string, logger *zap.Logger, key, bucket, awsRegion string) [][]byte {
	// Initializing variables
	logs := make([][]byte, 0)
	var logsJsons []map[string]interface{}

	// Process logs
	controlTowerParsing := getControlTowerParsing()
	for _, s3Log := range s3Logs {
		if len(s3Log) == 0 {
			continue
		}
		logsJsons = []map[string]interface{}{{fieldMessage: s3Log}}
		logs = addFieldsAndAppendLogsToFinalList(logs, logsJsons, logger, key, bucket, awsRegion, controlTowerParsing)
	}
	return logs
}

func processJsonLogs(s3Logs []string, logger *zap.Logger, key, bucket, awsRegion string) [][]byte {
	// Initializing variables
	logs := make([][]byte, 0)

	// Process logs
	controlTowerParsing := getControlTowerParsing()
	for _, s3Log := range s3Logs {
		if len(s3Log) == 0 {
			continue
		}

		var logsJsons []map[string]interface{}
		err := json.Unmarshal([]byte(s3Log), &logsJsons)

		if err != nil {
			logger.Error(fmt.Sprintf("Error occurred while trying to marshal json log: %s", err.Error()))
			logger.Error("Will try to send as a regular string...")
			logsJsons = []map[string]interface{}{{fieldMessage: s3Log}}
		}
		logs = addFieldsAndAppendLogsToFinalList(logs, logsJsons, logger, key, bucket, awsRegion, controlTowerParsing)
	}
	return logs
}

func addFieldsAndAppendLogsToFinalList(logs [][]byte, logsJsons []map[string]interface{}, logger *zap.Logger, key, bucket, awsRegion string, controlTowerParsing string) [][]byte {
	for _, logJson := range logsJsons {
		addLogzioFields(logJson, bucket, key, awsRegion)
		if len(controlTowerParsing) > 0 {
			addControlTowerParsing(controlTowerParsing, key, logJson, logger)
		}

		logBytes, err := json.Marshal(logJson)
		if err != nil {
			logger.Error(fmt.Sprintf("Error occurred while processing %s: %s", logJson, err.Error()))
			logger.Error("log will be dropped")
		}

		if logBytes != nil && len(logBytes) > 0 {
			logger.Debug(fmt.Sprintf("Adding log %s to logs list", string(logBytes)))
			logs = append(logs, logBytes)
		}
	}
	return logs
}

func addLogzioFields(logzioLog map[string]interface{}, bucket, key, awsRegion string) {
	objFullPath := fmt.Sprintf("%s/%s", bucket, key)
	logzioLog[fieldType] = getLogType()
	logzioLog[fieldS3Key] = objFullPath
	logzioLog[fieldAwsRegion] = awsRegion
}

func getBody(buf *bytes.Buffer, logger *zap.Logger) string {
	// Try to decompress Gzip:
	tempBuf := *buf
	body, err := decompressGzip(&tempBuf)
	if err == nil {
		logger.Debug("body was Gzipped!")
		return string(body)
	}

	logger.Debug(fmt.Sprintf("Error from attempt to decompress gzip: %s", err.Error()))
	// Try to decompress Zip:
	tempBuf = *buf
	body, err = decompressZip(&tempBuf, logger)
	if err == nil {
		logger.Debug("body was Zipped!")
		return string(body)
	}
	logger.Debug(fmt.Sprintf("Error from attempt to decompress zip: %s", err.Error()))

	// Returning string as is
	logger.Debug("Could not decompress gzip or zip, returning the body as is")
	return buf.String()
}

func decompressZip(buf *bytes.Buffer, logger *zap.Logger) ([]byte, error) {
	var decompressed bytes.Buffer
	body, err := ioutil.ReadAll(buf)
	if err != nil {
		return nil, err
	}

	zipReader, err := zip.NewReader(bytes.NewReader(body), int64(len(body)))
	if err != nil {
		return nil, err
	}

	// Read all the files from zip archive
	for _, zipFile := range zipReader.File {
		unzippedFileBytes, err := readZipFile(zipFile)
		if err != nil {
			logger.Error(fmt.Sprintf("Encountered error while trying to read zip: %s", err.Error()))
			continue
		}

		decompressed.Write(unzippedFileBytes)
		decompressed.Write([]byte("\n"))
	}

	logger.Debug(fmt.Sprintf("Full decompressed:\n%s", string(decompressed.Bytes())))
	return decompressed.Bytes(), nil
}

func readZipFile(zf *zip.File) ([]byte, error) {
	f, err := zf.Open()
	if err != nil {
		return nil, err
	}
	defer f.Close()
	return ioutil.ReadAll(f)
}

func decompressGzip(buf *bytes.Buffer) ([]byte, error) {
	reader, err := gzip.NewReader(buf)

	if err != nil {
		return nil, err
	}

	defer reader.Close()

	var decompressed bytes.Buffer
	_, err = decompressed.ReadFrom(reader)
	if err != nil {
		return nil, err
	}

	return decompressed.Bytes(), nil
}

func addControlTowerParsing(controlTowerParsing, objectKey string, log map[string]interface{}, logger *zap.Logger) {
	parsingKeys := strings.Split(controlTowerParsing, "/")
	logger.Debug(fmt.Sprintf("received from user %d keys to add to log: %v", len(parsingKeys), parsingKeys))
	parsingValues := strings.Split(objectKey, "/")

	if len(parsingKeys) == len(parsingValues) {
		for index, pk := range parsingKeys {
			logger.Debug(fmt.Sprintf("Adding key: %s with value %s", pk, parsingValues[index]))
			log[pk] = parsingValues[index]
		}
	} else {
		logger.Warn(fmt.Sprintf("Expected %d keys (%s), but found %d values (%s). Skipping addition of the custom fields", len(parsingKeys), parsingKeys, len(parsingValues), parsingValues))
	}
}
