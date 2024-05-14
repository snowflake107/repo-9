import { UserConfigType } from "@/types";
import {
  blueSkyIcon,
  facebookIcon,
  githubIcon,
  instagramIcon,
  linkedinIcon,
  mastodonIcon,
  snapchatIcon,
  telegramIcon,
  threadsIcon,
  whatsappIcon,
  xIcon,
  youtubeIcon,
  logodcc,
  Discord
} from "@/assets";


const userConfig: UserConfigType = {
  avatarSrc: "/assets/logodcc.png",
  avatarAlt: "Avatar",
  fullName: "DCC",
  alias: "@dcc",
  metaTitle: "LinkFolio",
  metaDescription: "A hub for all your online links 🔗",
  socialNetworks: [
    {
      url: "https://twitter.com/dccnita?t=wa7G9AW_mHU1jYi5Mfml-Q&s=08",
      iconSrc: xIcon,
      title: "Twitter / X",
      description: "@dccnita",
    },
    {
      url: "https://github.com/Developers-and-Coders-Club",
      iconSrc: githubIcon,
      title: "GitHub",
      description: "Develop with DCC",
    },
    {
      url: "https://www.linkedin.com/company/dccnita/",
      iconSrc: linkedinIcon,
      title: "LinkedIn",
      description: "Connect with DCC! 🌐",
    },
    
    {
      url: "https://www.instagram.com/dccnita/",
      iconSrc: instagramIcon,
      title: "Instagram",
      description: "Our official insta handle 📷",
    },
   
    {
      url: "#",
      iconSrc: whatsappIcon,
      title: "WhatsApp",
      description: "Simple, reliable messaging and calling 🟢",
    },
    {
      url: "https://t.me/+IrV38R0MAd02YmY1",
      iconSrc: telegramIcon,
      title: "Telegram",
      description: "Messaging focusing on speed and security 🚀",
    },
    {
      url: "https://dccnita.in/",
      iconSrc: logodcc,
      title: "Official Website",
      description: " Dream Code Conquer🌟",
    },
    {
      url: "bit.ly/dccResources",
      iconSrc: logodcc,
      title: "Resources",
      description: "Link for resources  💙",
    },
    {
      url: "https://cphub.dccnita.in/",
      iconSrc: logodcc,
      title: "CP Hub",
      description: "Competitive Programming hub ",
    },
    {
      url: "https://twitter.com/dccnita?t=wa7G9AW_mHU1jYi5Mfml-Q&s=08",
      iconSrc: threadsIcon,
      title: "Threads",
      description: "Quick updates and stories! 🌀",
    },
    {
      url: "https://www.youtube.com/@DCCNITA",
      iconSrc: youtubeIcon,
      title: "YouTube",
      description: "Discover, watch, and share your passion 🎥",
    },
    {
      url: "https://discord.gg/Ta84z5K5Vb",
      iconSrc: Discord,
      title: "Discord",
      description: "Connect with DCC on discord",
    },
    
    
  ],
};

export default userConfig;
