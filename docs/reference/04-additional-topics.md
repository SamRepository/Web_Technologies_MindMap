<!-- GENERATED FILE -- do not edit.
     Source of truth: concepts/**/*.yml
     Regenerate with: python scripts/build.py -->

# Additional Topics

## Version Control

### Git {#git}

A distributed version-control system for tracking changes in source code during software development.

- [Official Website](https://git-scm.com/)
- [Wikipedia](https://en.wikipedia.org/wiki/Git)
- [YouTube Resource CS50](https://youtu.be/NcoBAfJ6l2Q?si=W8uoDwk_akNihWOF)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%BA%D9%8A%D8%AA_%28%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D8%AC%29)

### GitHub {#github}

A code hosting platform for version control and collaboration, allowing developers to manage and store their code using Git.

- [Official Website](https://github.com/)
- [Wikipedia](https://en.wikipedia.org/wiki/GitHub)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%BA%D9%8A%D8%AA_%D9%87%D8%A7%D8%A8)

## Deployment

### Virtualization {#virtualization}

Virtualization is the process of creating virtual instances of physical resources, such as servers, storage, or networks. By using software like hypervisors, multiple virtual machines (VMs) can run on a single physical machine, optimizing resource use and providing flexibility in cloud environments. Virtualization is a key technology in cloud computing, enabling efficient allocation of computing resources and isolation of environments for security and scalability.

- [Wikipedia](https://en.wikipedia.org/wiki/Virtualization)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%85%D8%AD%D8%A7%D9%83%D8%A7%D8%A9_%D8%A7%D9%81%D8%AA%D8%B1%D8%A7%D8%B6%D9%8A%D8%A9)

### Cloud Computing {#cloud-computing}

Cloud computing delivers computing services—such as servers, storage, databases, and software—over the internet. It offers flexibility, scalability, and cost-efficiency, eliminating the need for on-premise infrastructure. Main service models include: Cloud computing is essential for modern web development, offering resources on demand.

- [Wikipedia](https://en.wikipedia.org/wiki/Cloud_computing)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AD%D9%88%D8%B3%D8%A8%D8%A9_%D8%B3%D8%AD%D8%A7%D8%A8%D9%8A%D8%A9)

- <span id="iaas"></span>**IaaS (Infrastructure as a Service)**: Virtualized computing resources like servers and storage (e.g., AWS EC2, Azure).

- <span id="paas"></span>**PaaS (Platform as a Service)**: Platforms for developing and running applications without managing infrastructure (e.g., Google App Engine, Heroku).

- <span id="saas"></span>**SaaS (Software as a Service)**: Software delivered via the internet, usually on a subscription basis (e.g., Google Workspace, Salesforce).

- <span id="heroku"></span>**Heroku** `legacy`: A cloud platform as a service (PaaS) supporting several programming languages, used for deploying, managing, and scaling applications.
  - [Official Website](https://www.heroku.com/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Heroku)

- <span id="aws"></span>**AWS**: Amazon Web Services (AWS) offers a suite of cloud computing services that make up an on-demand computing platform.
  - [Official Website](https://aws.amazon.com/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Amazon_Web_Services)
  - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AE%D8%AF%D9%85%D8%A7%D8%AA_%D8%A3%D9%85%D8%A7%D8%B2%D9%88%D9%86_%D9%88%D9%8A%D8%A8)

- <span id="gcp"></span>**GCP**: Google Cloud Platform (GCP) is a suite of cloud computing services offered by Google. It provides a range of services for computing, storage, data analytics, machine learning, and application development, all running on the same infrastructure that Google uses internally for its products like Google Search and YouTube. GCP enables businesses to build, deploy, and scale applications efficiently on a global network.
  - [Official Website](https://cloud.google.com/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Google_Cloud_Platform)
  - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%85%D9%86%D8%B5%D8%A9_%D8%AC%D9%88%D8%AC%D9%84_%D8%A7%D9%84%D8%B3%D8%AD%D8%A7%D8%A8%D9%8A%D8%A9)

## Performance Optimization

### SEO {#seo}

Search Engine Optimization are set of practices for increasing the quantity and quality of traffic to your website through organic search engine results.

- [Wikipedia](https://en.wikipedia.org/wiki/Search_engine_optimization)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AA%D8%AD%D8%B3%D9%8A%D9%86_%D9%85%D8%AD%D8%B1%D9%83%D8%A7%D8%AA_%D8%A7%D9%84%D8%A8%D8%AD%D8%AB)

### Caching {#caching}

The process of storing copies of files in a cache, or temporary storage location, so they can be accessed more quickly.

- [Wikipedia](https://en.wikipedia.org/wiki/Cache_(computing))
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%B0%D8%A7%D9%83%D8%B1%D8%A9_%D9%85%D8%AE%D8%A8%D8%A6%D9%8A%D8%A9)

### Minification {#minification}

The process of removing unnecessary characters from code to reduce its size, improving load times and performance.

- [Wikipedia](https://en.wikipedia.org/wiki/Minification_(programming))

### Core Web Vitals {#core-web-vitals}

Google's set of field metrics for user-perceived performance, measured on real visits rather than in a lab. They give the vaguer goal of "make it fast" three specific numbers to move, and they feed into search ranking.

- [web.dev — Web Vitals](https://web.dev/articles/vitals)

- <span id="lcp"></span>**LCP (Largest Contentful Paint)**: How long until the largest element in the viewport has rendered — a proxy for when the page looks loaded to the person waiting.
  - [web.dev — LCP](https://web.dev/articles/lcp)

- <span id="inp"></span>**INP (Interaction to Next Paint)**: How long the page takes to visibly respond to user input, across the whole visit. It replaced First Input Delay, which only measured the first interaction and so missed most of the problem.
  - [web.dev — INP](https://web.dev/articles/inp)

- <span id="cls"></span>**CLS (Cumulative Layout Shift)**: How much visible content moves around unexpectedly while loading — the metric for the page that shifts just as you go to tap something.
  - [web.dev — CLS](https://web.dev/articles/cls)

## Emerging Technologies

### WebAssembly {#webassembly}

WebAssembly (Wasm) is a binary instruction format for a stack-based virtual machine, enabling high-performance applications on web pages. It is designed as a portable compilation target for programming languages, enabling deployment on the web for client and server applications.

- [Official Website](https://webassembly.org/)
- [Wikipedia](https://en.wikipedia.org/wiki/WebAssembly)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%88%D9%8A%D8%A8_%D8%A3%D8%B3%D9%85%D8%A8%D9%84%D9%8A)

### GraphQL {#graphql}

GraphQL is a query language for your API, and a server-side runtime for executing queries by using a type system you define for your data. It provides a more efficient, powerful, and flexible alternative to REST.

- [Official Website](https://graphql.org/)
- [Wikipedia](https://en.wikipedia.org/wiki/GraphQL)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%BA%D8%B1%D8%A7%D9%81_%D9%83%D9%8A%D9%88_%D8%A5%D9%84)

### Hydration {#hydration}

Hydration is a technique used in web development, particularly in Single Page Applications (SPAs), where server-rendered HTML is enhanced with client-side JavaScript. This allows the page to become interactive by "hydrating" static content with dynamic behavior without requiring a full page reload.

- [Wikipedia](https://en.m.wikipedia.org/wiki/Hydration_(web_development))

- <span id="spas"></span>**SPAs (Single Page Applications)**: SPAs are web applications that load a single HTML page and dynamically update content as the user interacts with the app. This provides a seamless user experience by eliminating the need for full page reloads. Examples of SPAs include Gmail and Google Maps.
  - [Wikipedia](https://en.wikipedia.org/wiki/Single-page_application)
  - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AA%D8%B7%D8%A8%D9%8A%D9%82_%D8%A7%D9%84%D8%B5%D9%81%D8%AD%D8%A9_%D8%A7%D9%84%D9%88%D8%A7%D8%AD%D8%AF%D8%A9_%28%D9%88%D9%8A%D8%A8%29)

### JAMStack {#jamstack}

JAMStack (JavaScript, APIs, and Markup) is a modern web development architecture that decouples the front-end from the back-end. It involves building fast, secure web apps with pre-rendered static files served over a CDN, while APIs handle dynamic functionality. JAMStack enhances performance and scalability.

- [Wikipedia](https://en.wikipedia.org/wiki/Jamstack)

### WebGPU `emerging` {#webgpu}

A browser API exposing modern GPU capability for both rendering and general computation, succeeding WebGL. It makes serious graphics work and in-browser machine-learning inference practical on the web platform.

- [WebGPU](https://www.w3.org/TR/webgpu/)
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API)
- [Wikipedia](https://en.wikipedia.org/wiki/WebGPU)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%88%D9%8A%D8%A8_%D8%AC%D9%8A_%D8%A8%D9%8A_%D9%8A%D9%88)

### WebRTC {#webrtc}

A set of APIs for real-time audio, video and data directly between browsers, without a plugin and, once connected, often without relaying through a server. It underpins most browser-based calling and conferencing.

- [Official Website](https://webrtc.org/)
- [WebRTC](https://www.w3.org/TR/webrtc/)
- [Wikipedia](https://en.wikipedia.org/wiki/WebRTC)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%88%D9%8A%D8%A8_%D8%A2%D8%B1_%D8%AA%D9%8A_%D8%B3%D9%8A)

## Advanced Web Technologies

### Web Components {#web-components}

Web Components are a set of web platform APIs that allow you to create new, reusable, encapsulated HTML tags to use in web pages and web apps.

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Web_Components)
- [Wikipedia](https://en.wikipedia.org/wiki/Web_Components)

### Progressive Web Apps (PWAs) {#progressive-web-apps}

Progressive Web Apps are web applications that have been enhanced with modern web technologies to deliver an app-like experience to users. They can work offline, send push notifications, and be installed on a device's home screen.

- [Google Developers Guide](https://developers.google.com/web/progressive-web-apps)
- [Wikipedia](https://en.wikipedia.org/wiki/Progressive_web_application)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AA%D8%B7%D8%A8%D9%8A%D9%82_%D9%88%D9%8A%D8%A8_%D8%AA%D9%82%D8%AF%D9%85%D9%8A)

- <span id="service-workers"></span>**Service Workers**: A script the browser runs separately from the page, able to intercept its network requests. This is the machinery that lets a web app serve cached content offline and receive push notifications.
  - [Service Workers](https://www.w3.org/TR/service-workers/)
  - [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)

### Serverless Architecture {#serverless-architecture}

Serverless architecture is a cloud computing execution model in which the cloud provider runs the server, and dynamically manages the allocation of machine resources.

- [AWS Serverless](https://aws.amazon.com/serverless/)
- [Wikipedia](https://en.wikipedia.org/wiki/Serverless_computing)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AD%D9%88%D8%B3%D8%A8%D8%A9_%D8%B9%D8%AF%D9%8A%D9%85%D8%A9_%D8%A7%D9%84%D8%AE%D8%A7%D8%AF%D9%85)

### Kubernetes {#kubernetes}

Kubernetes is an open-source container-orchestration system for automating software deployment, scaling, and management.

- [Official Website](https://kubernetes.io/)
- [Wikipedia](https://en.wikipedia.org/wiki/Kubernetes)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%83%D9%88%D8%A8%D9%8A%D8%B1%D9%86%D9%8A%D8%AA%D9%8A%D8%B3)

### Docker {#docker}

Docker is a set of platform-as-a-service products that use OS-level virtualization to deliver software in packages called containers.

- [Official Website](https://www.docker.com/)
- [Wikipedia](https://en.wikipedia.org/wiki/Docker_(software))
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AF%D9%88%D9%83%D8%B1)

## AI-Era Web

### LLMs (Large Language Models) {#llm}

Models trained on very large text corpora that predict continuations of a prompt, and in doing so perform tasks they were not explicitly programmed for. Accessed over HTTP APIs, they have become an ordinary component of web applications rather than a specialist research tool.

- [Wikipedia](https://en.wikipedia.org/wiki/Large_language_model)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%86%D9%85%D9%88%D8%B0%D8%AC_%D9%84%D8%BA%D9%88%D9%8A_%D9%83%D8%A8%D9%8A%D8%B1)

### Prompt Engineering {#prompt-engineering}

Structuring the input to a language model — instructions, context, examples and output format — to get reliable results. It matters because the same underlying model can succeed or fail on a task depending on how the request is framed.

- [Wikipedia](https://en.wikipedia.org/wiki/Prompt_engineering)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%87%D9%86%D8%AF%D8%B3%D8%A9_%D8%A7%D9%84%D8%AA%D9%84%D9%82%D9%8A%D9%86)

### Embeddings {#embeddings}

Numeric vectors representing text, images or other data such that items close in meaning are close in the vector space. They are what makes search by meaning rather than by keyword possible.

- [Wikipedia](https://en.wikipedia.org/wiki/Word_embedding)

### RAG (Retrieval-Augmented Generation) {#rag}

Retrieving relevant documents and supplying them to a language model as context before it answers. It grounds answers in a specific corpus, which reduces fabrication and lets a model use information it was never trained on without retraining.

- [Wikipedia](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
- [Original paper (arXiv 2005.11401)](https://arxiv.org/abs/2005.11401)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AA%D9%88%D9%84%D9%8A%D8%AF_%D9%85%D8%B9%D8%B2%D8%B2_%D8%A8%D8%A7%D9%84%D8%A7%D8%B3%D8%AA%D8%AD%D8%B6%D8%A7%D8%B1)

### MCP (Model Context Protocol) `emerging` {#mcp}

An open protocol for connecting language models to external tools and data sources through a common interface, so an integration written once works across different clients instead of being rebuilt per application.

- [Official Website](https://modelcontextprotocol.io/)

### Streaming Responses {#streaming-responses}

Delivering a response incrementally as it is produced rather than waiting for it to complete, usually over Server-Sent Events or a readable stream. It is what makes a model's answer appear token by token instead of after a long pause.

- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Streams API](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API)

### AI Agents `emerging` {#ai-agents}

Systems in which a language model plans and carries out multi-step tasks by calling tools and reacting to the results, rather than only producing text. This is the classical notion of a software agent, with a model supplying the decision-making.

- [Wikipedia](https://en.wikipedia.org/wiki/Intelligent_agent)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%88%D9%83%D9%8A%D9%84_%D8%B0%D9%83%D9%8A)

## Industry Standards and Practices

### Agile {#agile}

Agile is a set of principles for software development under which requirements and solutions evolve through the collaborative effort of self-organizing and cross-functional teams.

- [Agile Manifesto](https://agilemanifesto.org/)
- [Wikipedia](https://en.wikipedia.org/wiki/Agile_software_development)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%A3%D8%AC%D8%A7%D9%8A%D9%84_%28%D9%85%D8%A8%D8%A7%D8%AF%D8%A6_%D8%AA%D8%B7%D9%88%D9%8A%D8%B1_%D8%A8%D8%B1%D9%85%D8%AC%D9%8A%D8%A7%D8%AA%29)

### Scrum {#scrum}

Scrum is an Agile framework for managing work with an emphasis on software development. It is designed for teams of ten or fewer members who break their work into goals that can be completed within time-boxed iterations.

- [Scrum.org](https://www.scrum.org/)
- [Wikipedia](https://en.wikipedia.org/wiki/Scrum_(software_development))
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%B3%D9%83%D8%B1%D9%85_%28%D8%AA%D8%B7%D9%88%D9%8A%D8%B1_%D8%A7%D9%84%D8%A8%D8%B1%D9%85%D8%AC%D9%8A%D8%A7%D8%AA%29)

### DevOps {#devops}

DevOps is a set of practices that combines software development (Dev) and IT operations (Ops). It aims to shorten the systems development life cycle and provide continuous delivery with high software quality.

- [Official Guide](https://aws.amazon.com/devops/what-is-devops/)
- [Wikipedia](https://en.wikipedia.org/wiki/DevOps)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AF%D9%8A%D9%81_%D8%A3%D9%88%D8%A8%D8%B3)
