# Interactive E-Book for Children: "Alice's Wonderland"

## Overview

In an era where traditional reading habits are declining across all age groups, largely due to the allure of more dynamic and quickly consumed media like TikTok or Instagram videos, this project aims to leverage technology to promote reading among children. By creating an interactive e-book that provides an engaging and educational experience, we hope to rekindle the joy of literature in young readers.

### Technical Overview

- **Business Understanding**: Addressing the trend of declining reading habits by using technology to promote literature.
- **Analytics Approach**: A web-based project that gathers continuous feedback from users to enhance the reading experience.
- **Data Requirements & Collection**: Content from "Alice's Wonderland" and art-style aligned illustrations will be used to train text-to-image diffusion models.

### Data Understanding & Preparation

Filtering data from the book and images for model training. For feedback analysis, common usability data will be visualized in charts, and questions will be categorized by character names and keywords.

- **Embedded Data Storage**: VectorDB
- **Feedback Data Storage**: MongoDB or SQLalchemy

### Modeling

Using LangChain for text processing tasks such as chunk splitting, chat memory management, and token size adjustments. Depending on resource availability, either a local LLM or OpenAI's models will be used.

### Evaluation & Feedback

Using embedding-based metrics and statistical data from usability charts to measure the effectiveness of the interactive e-book.

## Personal Project Ideation

**Creator**: Daniel Djinishiande Briquez
**Affiliation**: Fontys AI 2024 Minor

## Summary & Societal Impact

The project's goal is to create an immersive interactive e-book specifically designed for children. This e-book will feature AI-generated images and text boxes, and an interactive chat prompt that simulates a character from "Alice in Wonderland" with their own personality and knowledge base.

### Important Points

1. **Interactive Ebook Interface**
   - The e-book will have an attractive and easy-to-understand interface with various AI-generated images and visual elements tailored for children.
   - **Source**: Personal prototype with editing in progress.

2. **Interactive Chat**
   - The chat prompt will enable students to engage in a dialogue with characters from "Alice in Wonderland," fostering an active learning environment.

3. **Availability and Accessibility**
   - As a web-based project, the interactive e-book will be accessible to anyone, making education more accessible and aligned with current technologies.

---

*This README is based on the personal project ideation by Daniel Djinishiande Briquez as part of the Fontys AI group 2024 first semester.*
