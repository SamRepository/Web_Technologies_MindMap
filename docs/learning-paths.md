<!-- GENERATED FILE -- do not edit.
     Source of truth: paths/*.yml and concepts/**/*.yml
     Regenerate with: python scripts/build.py -->

# Learning Paths

The mind map is a reference: it is organised by *what things are*, not by the order you should meet them in. These paths are the missing second axis — a teaching sequence through the same concepts, with an estimate of what each stage costs in time.

| Path | Level | Duration | Effort | Concepts |
|---|---|---|---|---|
| [Front-End Foundations](#front-end-foundations) | `beginner` | 12 weeks | 77 hours | 55 |
| [Back-End with Python](#back-end-with-python) | `intermediate` | 14 weeks | 86 hours | 48 |
| [Full Stack](#full-stack) | `advanced` | 13 weeks | 85 hours | 44 |
| [Semantic Web & Knowledge Graphs](#semantic-web-and-knowledge-graphs) | `advanced` | 11 weeks | 66 hours | 37 |

Every entry below is a concept from the map, not a restatement of it. Paths reference concepts by id, so a definition corrected in one place is corrected everywhere, and a path can never cite something the map does not contain.

These paths sequence **145 of 193 concepts**. The remainder are in the map deliberately — reference material a student should be able to look up without a course walking them through it.

---

## Front-End Foundations {#front-end-foundations}

`beginner` · 12 weeks · 77 hours · about 6 h/week

From "what happens when I type a URL" to shipping an accessible, fast, component-based interface. Assumes no prior web experience.

**Who it is for.** First-year students and self-taught beginners. No prerequisite beyond comfort with a text editor and a command line.

**By the end.** You can build and deploy a multi-page site with a component framework, explain what the browser does with each file it receives, and name the threat each front-end defence exists to stop.

**Prerequisites.** None — this is a starting point.

### 1. How the web actually works {#front-end-foundations--1}

*1 week · 6 hours*

Before writing any markup, be able to describe the round trip: a name resolved, a connection opened, a request sent, a response rendered. Everything later in this path is a detail of that loop.

[Networking](reference/01-introduction.md#networking-2) · [Protocols](reference/01-introduction.md#protocols) · [TCP/IP](reference/01-introduction.md#tcp-ip) · [DNS](reference/01-introduction.md#dns) · [HTTP/HTTPS](reference/01-introduction.md#http-https) · [URI/URL](reference/01-introduction.md#uri-url) · [Browsers](reference/03-web-development.md#browsers) · [Client-Side](reference/03-web-development.md#client-side) · [Developer Mode](reference/03-web-development.md#developer-mode)

**Practice.** Open the browser's network panel on a site you use daily. Count the requests, find the slowest one, and identify which are documents, stylesheets, scripts and images.

### 2. Documents — HTML {#front-end-foundations--2}

*1 week · 6 hours*

Write markup that means something. Structure first, appearance later: a heading is a heading because of what it is, not how it looks.

[HTML/CSS](reference/03-web-development.md#html-css) · [Basic HTML](reference/02-evolution.md#basic-html) · [HTML5](reference/03-web-development.md#html5) · [W3C Consortium (World Wide Web Consortium)](reference/01-introduction.md#w3c-consortium)

**Practice.** Mark up a two-page CV with no CSS at all. It must still be readable and correctly ordered with styling disabled.

### 3. Presentation — CSS {#front-end-foundations--3}

*2 weeks · 12 hours*

Lay out a page with the tools designed for layout, rather than fighting floats. Grid and container queries are the modern default; a utility or component framework is a choice made on top of understanding them.

[CSS3](reference/03-web-development.md#css3) · [CSS Grid Layout](reference/03-web-development.md#css-grid) · [Container Queries](reference/03-web-development.md#container-queries) · [SCSS (Sassy CSS)](reference/03-web-development.md#scss) · [Bootstrap](reference/03-web-development.md#bootstrap) · [Tailwind CSS](reference/03-web-development.md#tailwind-css)

**Practice.** Rebuild the CV as a responsive two-column layout with CSS Grid, then make one component respond to its own width rather than the viewport's.

### 4. Programming the page {#front-end-foundations--4}

*2 weeks · 14 hours*

Manipulate the document from JavaScript, and understand why the library that once made this bearable is now largely unnecessary.

[JavaScript](reference/03-web-development.md#javascript) · [ES6+ features](reference/03-web-development.md#es6-features) · [DOM Manipulation](reference/03-web-development.md#dom-manipulation) · [jQuery](reference/03-web-development.md#jquery) *(legacy)*

**Practice.** Add client-side form validation with no library. Then read a jQuery snippet from an old tutorial and write down its modern equivalent.

### 5. Modules, types and tooling {#front-end-foundations--5}

*1 week · 7 hours*

Move from script tags to a real build. Understand what a bundler does before adopting one, so its failure modes are diagnosable.

[ES Modules (ESM)](reference/03-web-development.md#esm) · [Import Maps](reference/03-web-development.md#import-maps) · [TypeScript](reference/03-web-development.md#typescript) · [Vite](reference/03-web-development.md#vite) · [esbuild](reference/03-web-development.md#esbuild) · [Minification](reference/04-additional-topics.md#minification)

**Practice.** Convert the project to ES modules, add a Vite build, then compare the development and production output byte for byte.

### 6. Component frameworks {#front-end-foundations--6}

*2 weeks · 14 hours*

Learn one framework properly and recognise the family resemblance in the rest. Note that Angular and AngularJS are different projects — the second was retired in 2010 and is not a version of the first.

[Frameworks and Libraries](reference/03-web-development.md#frameworks-and-libraries) · [React.js](reference/03-web-development.md#react-js) · [Vue.js](reference/03-web-development.md#vue-js) · [Svelte](reference/03-web-development.md#svelte) · [Angular](reference/03-web-development.md#angular) · [AngularJS](reference/03-web-development.md#angularjs) *(legacy)* · [SPAs (Single Page Applications)](reference/04-additional-topics.md#spas) · [Hydration](reference/04-additional-topics.md#hydration)

**Practice.** Rebuild one page as components in a framework of your choice, and write a paragraph on what the framework saved you and what it cost you.

### 7. Fast and findable {#front-end-foundations--7}

*1 week · 6 hours*

Performance is measurable, so measure it. Core Web Vitals are the metrics that search engines actually use, which makes speed and discoverability the same conversation.

[Core Web Vitals](reference/04-additional-topics.md#core-web-vitals) · [LCP (Largest Contentful Paint)](reference/04-additional-topics.md#lcp) · [INP (Interaction to Next Paint)](reference/04-additional-topics.md#inp) · [CLS (Cumulative Layout Shift)](reference/04-additional-topics.md#cls) · [Caching](reference/04-additional-topics.md#caching) · [SEO](reference/04-additional-topics.md#seo)

**Practice.** Measure the three vitals on your own site, make one change to improve the worst of them, and measure again.

### 8. Front-end security {#front-end-foundations--8}

*1 week · 6 hours*

Understand each defence as an answer to a specific attack, not as a configuration ritual. CSP exists because of XSS; CORS exists because the same-origin policy would otherwise be too strict to be usable.

[Threats](reference/03-web-development.md#threats) · [XSS (Cross-Site Scripting)](reference/03-web-development.md#xss) · [CSRF (Cross-Site Request Forgery)](reference/03-web-development.md#csrf) · [CSP (Content Security Policy)](reference/03-web-development.md#content-security-policy) · [CORS (Cross-Origin Resource Sharing)](reference/03-web-development.md#cors) · [TLS / HTTPS](reference/03-web-development.md#tls-https)

**Practice.** Introduce a deliberate XSS hole in a local copy, exploit it, then close it with a Content Security Policy and confirm the exploit stops working.

### 9. Publishing {#front-end-foundations--9}

*1 week · 6 hours*

Get it onto the public web, under version control, in a way you can repeat tomorrow without remembering anything.

[Git](reference/04-additional-topics.md#git) · [GitHub](reference/04-additional-topics.md#github) · [Static Web Pages](reference/02-evolution.md#static-web-pages) · [JAMStack](reference/04-additional-topics.md#jamstack) · [Progressive Web Apps (PWAs)](reference/04-additional-topics.md#progressive-web-apps) · [Service Workers](reference/04-additional-topics.md#service-workers)

**Practice.** Deploy the site from a Git repository, then make it load once offline with a service worker.

---

## Back-End with Python {#back-end-with-python}

`intermediate` · 14 weeks · 86 hours · about 6 h/week

The server side of the same round trip: data modelling, two Python frameworks at different points on the batteries-included axis, APIs, the attacks that target them, and getting the result to run somewhere other than your laptop.

**Who it is for.** Students who have completed Front-End Foundations, or who can already build a static site and read JavaScript.

**By the end.** You can design a relational schema, expose it through a documented HTTP API, defend it against the standard attack classes, and deploy it in a container.

**Prerequisites.** [Front-End Foundations](#front-end-foundations)

### 1. Programming foundations {#back-end-with-python--1}

*1 week · 6 hours*

Establish the vocabulary the rest of the path assumes. A paradigm is a way of organising a program, not a language feature.

[Programming](reference/00-disciplines.md#programming) · [Paradigms](reference/00-pillars.md#paradigms) · [OOP (Object-Oriented Programming)](reference/03-web-development.md#oop) · [Algorithmic](reference/00-disciplines.md#algorithmic)

**Practice.** Take one procedural script you have written and restructure it around objects. Note honestly which parts got clearer and which got longer.

### 2. Server-side basics {#back-end-with-python--2}

*1 week · 6 hours*

Understand what a server process is and what it is doing between requests, before a framework hides it.

[Server-Side Programming](reference/03-web-development.md#server-side-programming) · [Server](reference/01-introduction.md#server) · [Python/PHP](reference/03-web-development.md#python-php) · [Python](reference/03-web-development.md#python)

**Practice.** Serve a page from a Python standard-library HTTP server, with no framework at all, and handle one POST by hand.

### 3. Relational data {#back-end-with-python--3}

*2 weeks · 12 hours*

Model data as relations and query it directly. SQL first, so the ORM later is a convenience rather than a mystery.

[Databases](reference/00-disciplines.md#databases) · [Databases](reference/03-web-development.md#databases-2) · [SQL](reference/03-web-development.md#sql)

**Practice.** Design a schema for a small library catalogue and answer five questions about it in raw SQL, including one join and one aggregate.

### 4. When relational is the wrong shape {#back-end-with-python--4}

*1 week · 6 hours*

Recognise the workloads that relational tables serve badly, and what each alternative family trades away to serve them better.

[NoSQL](reference/03-web-development.md#nosql) · [Graph Databases](reference/03-web-development.md#graph-databases) · [Vector Databases](reference/03-web-development.md#vector-databases) · [Big Data](reference/03-web-development.md#big-data)

**Practice.** Take the catalogue schema and write down what a graph store would make easy that SQL makes awkward — and what you would lose.

### 5. A small framework — Flask {#back-end-with-python--5}

*2 weeks · 12 hours*

Build a web application from explicit parts, where every piece of routing, templating and configuration is something you wrote.

[Web Frameworks](reference/03-web-development.md#web-frameworks) · [Flask](reference/03-web-development.md#flask) · [MVC](reference/03-web-development.md#mvc) · [Templating Engines](reference/03-web-development.md#templating-engines)

**Practice.** Build a CRUD interface over the catalogue with Flask and a template engine, with no ORM.

### 6. A batteries-included framework — Django {#back-end-with-python--6}

*2 weeks · 12 hours*

Contrast Flask's explicitness with a framework that makes the decisions for you, and see what an ORM buys and costs against the raw SQL you wrote.

[Django](reference/03-web-development.md#django) · [ORM (Object-Relational Mapping)](reference/03-web-development.md#orm)

**Practice.** Rebuild the same catalogue in Django, then inspect the SQL its ORM actually emits for your three most common queries.

### 7. APIs {#back-end-with-python--7}

*2 weeks · 12 hours*

Expose the data to clients you do not control. REST is the default; know when a graph query language or a persistent socket fits better.

[Web Services and APIs](reference/03-web-development.md#web-services-and-apis) · [RESTful APIs](reference/03-web-development.md#restful-apis) · [JSON](reference/01-introduction.md#json) · [Data Exchange Formats](reference/01-introduction.md#data-exchange-formats) · [GraphQL](reference/04-additional-topics.md#graphql) · [WebSockets](reference/03-web-development.md#websockets)

**Practice.** Publish the catalogue as a JSON API, consume it from the front end you built in the previous path, and fix the CORS error you will get.

### 8. Securing it {#back-end-with-python--8}

*1 week · 7 hours*

Attack your own application. Every defence in this module answers a specific one of the threats listed beside it.

[Threats](reference/03-web-development.md#threats) · [SQL Injection](reference/03-web-development.md#sql-injection) · [CSRF (Cross-Site Request Forgery)](reference/03-web-development.md#csrf) · [Phishing](reference/03-web-development.md#phishing) · [Defenses](reference/03-web-development.md#defenses) · [TLS / HTTPS](reference/03-web-development.md#tls-https) · [WebAuthn and Passkeys](reference/03-web-development.md#webauthn-passkeys)

**Practice.** Write a deliberately vulnerable query, exploit it with SQL injection, then fix it with parameter binding and confirm the exploit fails.

### 9. Running it somewhere else {#back-end-with-python--9}

*1 week · 7 hours*

Separate "works on my machine" from "works". Understand the ladder from a virtual machine to a managed platform to no server at all.

[Virtualization](reference/04-additional-topics.md#virtualization) · [Docker](reference/04-additional-topics.md#docker) · [Cloud Computing](reference/04-additional-topics.md#cloud-computing) · [IaaS (Infrastructure as a Service)](reference/04-additional-topics.md#iaas) · [PaaS (Platform as a Service)](reference/04-additional-topics.md#paas) · [SaaS (Software as a Service)](reference/04-additional-topics.md#saas) · [Heroku](reference/04-additional-topics.md#heroku) *(legacy)* · [Serverless Architecture](reference/04-additional-topics.md#serverless-architecture)

**Practice.** Containerise the application, run it from the image on a clean machine, and list what the container still assumes about its environment.

### 10. Working like a team {#back-end-with-python--10}

*1 week · 6 hours*

The practices that make the previous nine modules survivable with other people involved.

[Software Engineering](reference/00-disciplines.md#software-engineering) · [Agile](reference/04-additional-topics.md#agile) · [Scrum](reference/04-additional-topics.md#scrum) · [DevOps](reference/04-additional-topics.md#devops) · [Git](reference/04-additional-topics.md#git) · [GitHub](reference/04-additional-topics.md#github)

**Practice.** Put the project under version control with a branch per feature, and set up one automated check that runs on every push.

---

## Full Stack {#full-stack}

`advanced` · 13 weeks · 85 hours · about 7 h/week

Joining the two halves: rendering strategies that span client and server, realtime transport, browser platform APIs, and a substantial block on ERP development with Odoo — the stack this course is taught around.

**Who it is for.** Students who have completed both Front-End Foundations and Back-End with Python, or who work across both already.

**By the end.** You can choose a rendering strategy and defend the choice, build against a real ERP framework, and take the result from a container to an orchestrated deployment.

**Prerequisites.** [Front-End Foundations](#front-end-foundations), [Back-End with Python](#back-end-with-python)

### 1. Where the work happens {#full-stack--1}

*1 week · 7 hours*

The central full-stack question is not which framework but which machine does the rendering, and when. Everything downstream follows from that.

[MVC](reference/03-web-development.md#mvc) · [Client-Side](reference/03-web-development.md#client-side) · [Server-Side Programming](reference/03-web-development.md#server-side-programming) · [RESTful APIs](reference/03-web-development.md#restful-apis)

**Practice.** Draw the request lifecycle for the same page rendered three ways: fully on the server, fully in the browser, and split between them.

### 2. Meta-frameworks {#full-stack--2}

*2 weeks · 14 hours*

Frameworks that answer the previous module's question for you. Learn what each one has decided on your behalf.

[Meta-Frameworks](reference/03-web-development.md#meta-frameworks) · [Next.js](reference/03-web-development.md#next-js) · [Nuxt](reference/03-web-development.md#nuxt) · [SvelteKit](reference/03-web-development.md#sveltekit) · [Remix](reference/03-web-development.md#remix) · [Astro](reference/03-web-development.md#astro) · [Hydration](reference/04-additional-topics.md#hydration) · [JAMStack](reference/04-additional-topics.md#jamstack)

**Practice.** Build the same three-page app twice, in two different meta-frameworks, and compare the shipped JavaScript payload.

### 3. Realtime and streaming {#full-stack--3}

*1 week · 7 hours*

Not every interaction fits request-and-response. Know the three transports and which problem each was built for.

[WebSockets](reference/03-web-development.md#websockets) · [Streaming Responses](reference/04-additional-topics.md#streaming-responses) · [WebRTC](reference/04-additional-topics.md#webrtc)

**Practice.** Add a live-updating view over a WebSocket, then implement the same feature with polling and measure the difference in requests and latency.

### 4. The browser as a platform {#full-stack--4}

*2 weeks · 12 hours*

Capabilities that used to require a native application: background code, offline storage, a component model without a framework, and near-native compute.

[Progressive Web Apps (PWAs)](reference/04-additional-topics.md#progressive-web-apps) · [Service Workers](reference/04-additional-topics.md#service-workers) · [Web Components](reference/04-additional-topics.md#web-components) · [WebAssembly](reference/04-additional-topics.md#webassembly) · [WebGPU](reference/04-additional-topics.md#webgpu)

**Practice.** Make the app installable and usable offline, and write one custom element that works with no framework present.

### 5. ERP and the Odoo stack {#full-stack--5}

*3 weeks · 21 hours*

A full-stack framework from a different tradition, where the data model is the application. Note that Odoo's OWL is the Odoo Web Library, unrelated to the Web Ontology Language of the semantic-web path.

[Information Systems](reference/00-disciplines.md#information-systems) · [ERP Systems](reference/03-web-development.md#erp-systems) · [Odoo Framework](reference/03-web-development.md#odoo-framework) · [ORM (Object-Relational Mapping)](reference/03-web-development.md#orm) · [OWL (Odoo Web Library)](reference/03-web-development.md#owl-odoo-web-library) · [Templating Engines](reference/03-web-development.md#templating-engines) · [QWeb](reference/03-web-development.md#qweb)

**Practice.** Build a small Odoo module with its own model, a QWeb view and an OWL component, and explain which of the three the ORM is driving.

### 6. Containers and orchestration {#full-stack--6}

*2 weeks · 12 hours*

One container is a packaging decision; many containers is an architecture. Know where the boundary sits and what crossing it costs.

[Virtualization](reference/04-additional-topics.md#virtualization) · [Docker](reference/04-additional-topics.md#docker) · [Kubernetes](reference/04-additional-topics.md#kubernetes) · [Serverless Architecture](reference/04-additional-topics.md#serverless-architecture) · [Cloud Computing](reference/04-additional-topics.md#cloud-computing)

**Practice.** Compose the application and its database as two containers, then write down what you would have to solve before running three replicas.

### 7. Performance in production {#full-stack--7}

*1 week · 6 hours*

The same metrics as the front-end path, now with a server, a database and a cache in the path — where most of the latency actually lives.

[Core Web Vitals](reference/04-additional-topics.md#core-web-vitals) · [Caching](reference/04-additional-topics.md#caching) · [Minification](reference/04-additional-topics.md#minification) · [SEO](reference/04-additional-topics.md#seo)

**Practice.** Profile a slow page end to end and attribute the time to network, server, query and render. Fix whichever dominates.

### 8. Delivering as a team {#full-stack--8}

*1 week · 6 hours*

Tooling and process for work that no longer fits in one person's head.

[Agile](reference/04-additional-topics.md#agile) · [Scrum](reference/04-additional-topics.md#scrum) · [DevOps](reference/04-additional-topics.md#devops) · [Git](reference/04-additional-topics.md#git) · [GitHub](reference/04-additional-topics.md#github) · [IDEs (Integrated Development Environments)](reference/03-web-development.md#ides) · [VS Code](reference/03-web-development.md#vs-code) · [PyCharm](reference/03-web-development.md#pycharm)

**Practice.** Set up continuous integration that runs the test suite and refuses a merge when it fails.

---

## Semantic Web & Knowledge Graphs {#semantic-web-and-knowledge-graphs}

`advanced` · 11 weeks · 66 hours · about 6 h/week

Web 3.0 as the W3C meant it: making data machine-readable through identifiers, RDF, ontologies and query. Ends where this material now meets language models, which is the live research question rather than a footnote.

**Who it is for.** Students with some web development behind them who want the data layer, and anyone approaching knowledge graphs from a database or AI direction.

**By the end.** You can model a domain in RDF, express constraints in an ontology, query it with SPARQL, and explain precisely how a knowledge graph and a vector index answer different questions about the same corpus.

**Prerequisites.** [Front-End Foundations](#front-end-foundations)

### 1. What Web 3.0 means here {#semantic-web-and-knowledge-graphs--1}

*1 week · 5 hours*

Settle the terminology before it causes trouble. In this course Web 3.0 is the Semantic Web; "Web3" is a later and separate coinage from the cryptocurrency industry. Both appear in the literature you will read.

[Web3 vs Web 3.0 — a note on terminology](reference/02-evolution.md#web3-disambiguation) · [Static Web Pages](reference/02-evolution.md#static-web-pages) · [Dynamic and Interactive Web](reference/02-evolution.md#dynamic-and-interactive-web) · [Social Media Integration](reference/02-evolution.md#social-media-integration) · [Blockchain and Decentralization](reference/02-evolution.md#blockchain-and-decentralization)

**Practice.** Find three articles using "Web3" and classify each by which of the two meanings the author intends. Some will not be decidable — say so.

### 2. Identity and encoding {#semantic-web-and-knowledge-graphs--2}

*1 week · 6 hours*

Everything downstream is built on being able to name a thing unambiguously and write that name down. IRIs are what let those names leave ASCII.

[URI/URL](reference/01-introduction.md#uri-url) · [IRI (Internationalized Resource Identifier)](reference/01-introduction.md#iri) · [Data Encoding](reference/01-introduction.md#data-encoding) · [Unicode](reference/01-introduction.md#unicode) · [UTF-8](reference/01-introduction.md#utf-8) · [UTF-16](reference/01-introduction.md#utf-16) · [Unicode, Inc. (Unicode Consortium)](reference/01-introduction.md#unicode-inc)

**Practice.** Take ten entities from a domain you know and mint a URI for each. Justify why yours will still resolve in ten years, or admit that it will not.

### 3. Exchange formats {#semantic-web-and-knowledge-graphs--3}

*1 week · 6 hours*

The serialisations RDF arrives in, and the tree-shaped formats it is usually confused with.

[Data Exchange Formats](reference/01-introduction.md#data-exchange-formats) · [XML](reference/01-introduction.md#xml) · [XPath (XML Path Language)](reference/01-introduction.md#xpath) · [JSON](reference/01-introduction.md#json) · [CSV (Comma-Separated Values)](reference/01-introduction.md#csv)

**Practice.** Express the same five facts as XML, as JSON and as a CSV table, then note which relationships each format cannot state without a convention.

### 4. RDF and linked data {#semantic-web-and-knowledge-graphs--4}

*2 weeks · 12 hours*

The triple as the unit of meaning, and the four principles that make a collection of triples a web rather than a file.

[Linked Data](reference/02-evolution.md#linked-data) · [RDF/ RDFS](reference/02-evolution.md#rdf-rdfs) · [W3C Consortium (World Wide Web Consortium)](reference/01-introduction.md#w3c-consortium)

**Practice.** Publish your ten entities as RDF, linking at least three of them to identifiers on an existing public dataset rather than inventing your own.

### 5. Ontologies and rules {#semantic-web-and-knowledge-graphs--5}

*2 weeks · 12 hours*

Move from describing data to constraining it. What a reasoner can derive that was never explicitly written down is the whole point.

[OWL](reference/02-evolution.md#owl) · [SWRL/RIF](reference/02-evolution.md#swrl-rif)

**Practice.** Write an ontology for your domain with two class hierarchies and one property restriction, then run a reasoner and inspect what it inferred.

### 6. Querying graphs {#semantic-web-and-knowledge-graphs--6}

*1 week · 7 hours*

SPARQL against RDF, set beside the SQL you already know. The comparison is the fastest way to see what graph query buys you.

[SPARQL](reference/02-evolution.md#sparql) · [SQL](reference/03-web-development.md#sql) · [Graph Databases](reference/03-web-development.md#graph-databases)

**Practice.** Write the same question as a SPARQL query and a SQL query over equivalent data, and compare what each needs you to know about the schema in advance.

### 7. Knowledge graphs in practice {#semantic-web-and-knowledge-graphs--7}

*1 week · 6 hours*

What changes at scale, and why industrial knowledge graphs look different from the textbook version.

[Knowledge Graphs](reference/02-evolution.md#knowledge-graphs) · [Databases](reference/03-web-development.md#databases-2) · [Big Data](reference/03-web-development.md#big-data)

**Practice.** Load a public knowledge graph extract and answer one question that would require three joins in a relational schema.

### 8. Where this meets language models {#semantic-web-and-knowledge-graphs--8}

*2 weeks · 12 hours*

Embeddings retrieve by similarity; a knowledge graph answers by structure. Retrieval-augmented generation uses the first, and increasingly wants the second. Knowing which failure belongs to which is the useful skill.

[AI (Artificial Intelligence)](reference/02-evolution.md#ai) · [LLMs (Large Language Models)](reference/04-additional-topics.md#llm) · [NLP](reference/02-evolution.md#nlp) · [Prompt Engineering](reference/04-additional-topics.md#prompt-engineering) · [Embeddings](reference/04-additional-topics.md#embeddings) · [Vector Databases](reference/03-web-development.md#vector-databases) · [RAG (Retrieval-Augmented Generation)](reference/04-additional-topics.md#rag) · [MCP (Model Context Protocol)](reference/04-additional-topics.md#mcp) · [AI Agents](reference/04-additional-topics.md#ai-agents)

**Practice.** Build a small RAG pipeline over your own documents, then find a question it answers wrongly and explain whether a graph would have got it right.

---
