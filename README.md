# Fedrit

Welcome to Fedrit, a web platform dedicated to fostering a more open, decentralized, and free internet. The aim of this project is to counteract the growing centralization of the internet and provide an alternative option to the major social media platforms that takes the role of the modern day public square, with a focus on the accountability and responsbility is required for any platform in such a position. The code is, and will always be, fully open source and easily deployable by anybody who wishes to operate their own platform/federation.

## Philosophy and Objectives

### Terminology

- **Platform:** An instance running the code. Each platform instance can host multiple communities, each with its own set of users and community rules. Communities created on one platform will also be accessible on any other platform that is federated with the originating platform the community was created on. The creators/moderators of any community will still retain their control over their community even on other platforms that are not the original community platform, as long as the two platforms are federated initially.
- **Community:** A community is a space created to serve as a central space for Users to discuss a common interest or goal. A community is specific to a platform but can be created by users from any federated platform and can exist independently from the original platform. The exact behavior/appearance of a community is highly customizable by the creators/managers of each community, some examples of possible community configurations are (optionally): a voting system, the ability to define content algorithm behaviour, the ability to dictacte community content layout (ie focus on images, only allow text, comments, ??), the ability to allow anonymous posting/voting, etc (and every combination thereof based on a specific community's needs!)
- **Manager:** An individual who created/moderates a community on a platform instance. While initially Users are created on a specific platform, users can identify themselves on other federated platforms even if the original platform no longer exists.


### Philosophy

The goal of this project is to tackle the issues of accountability, centralization, censorship, and privacy plaguing the current internet head-on by offering an alternative option which both focuses on these concerns as well as providing features that are not currently found anywhere else.

- **Decentralization:** Combat the increasing centralization of the internet by enabling users to create and control their own online communities, free from the influence of large corporations.
- **Transparency:** Operate the project with 100% transparency, disclosing all financial matters and ensuring all decisions are made openly. As an LLC, Fedrit commits to maintaining this transparency and encouraging the use of its code for anyone who wishes to create their own platform instance or federation.
- **Privacy and Internet Freedom:** Prioritize privacy and freedom, refraining from obtrusive advertising or data collection methods. Monetization will be ethical and secondary to the mission of making the internet a better place, focusing on options such as badges, awards, and easy-create-platform functionality.
- **Federated Architecture:** Users can create, join, and interact with communities hosted on different instances of the Fedrit code, enabling cross-platform collaboration.
- **Customizable Community Behavior:** Community creators can define the rules, appearance, and functionality of their communities, tailoring them to their specific needs and preferences.
- **Ethical Monetization:** Focus on ethical monetization methods such as selling awards, badges, or other virtual goods, while prioritizing privacy and user experience.

## Code Architecture and Infrastructure

I have tried to ensure the code quality is the best I can achieve. The backend is developed using Python 3 and the Django web framework, while the frontend is built with TypeScript and React.

**Key Components:**

- Backend: Python 3 + Django
- Frontend: TypeScript + React
- Database: SQLite (can be easily replaced with other database systems)
- API: Django REST Framework

## Getting Started

To get started with Fedrit, follow these simple steps:

1. Clone the repository.
2. Set up your development environment (Python, Node.js, etc.).
3. Install dependencies using pip for the backend and npm or yarn for the frontend.
4. Follow the configuration instructions in the documentation.
5. Run the development server for both backend and frontend.

```
docker run -it -p 80:80 -p 3000:3000 -p 8000:8000 fedrit
```