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
| [Semantic Web & Knowledge Graphs](#semantic-web--knowledge-graphs) | `advanced` | 11 weeks | 66 hours | 37 |

Every entry below is a concept from the map, not a restatement of it. Paths reference concepts by id, so a definition corrected in one place is corrected everywhere, and a path can never cite something the map does not contain.

These paths sequence **145 of 193 concepts**. The remainder are in the map deliberately — reference material a student should be able to look up without a course walking them through it.

Concept names below are plain text. On the [published site](https://samrepository.github.io/Web_Technologies_MindMap/reference/) each one links to its full definition and sources.

---

## Front-End Foundations

`beginner` · 12 weeks · 77 hours · about 6 h/week

From "what happens when I type a URL" to shipping an accessible, fast, component-based interface. Assumes no prior web experience.

**Who it is for.** First-year students and self-taught beginners. No prerequisite beyond comfort with a text editor and a command line.

**By the end.** You can build and deploy a multi-page site with a component framework, explain what the browser does with each file it receives, and name the threat each front-end defence exists to stop.

**Prerequisites.** None — this is a starting point.

### 1. How the web actually works

*1 week · 6 hours*

Before writing any markup, be able to describe the round trip: a name resolved, a connection opened, a request sent, a response rendered. Everything later in this path is a detail of that loop.

**Networking** · **Protocols** · **TCP/IP** · **DNS** · **HTTP/HTTPS** · **URI/URL** · **Browsers** · **Client-Side** · **Developer Mode**

**Practice.** Open the browser's network panel on a site you use daily. Count the requests, find the slowest one, and identify which are documents, stylesheets, scripts and images.

### 2. Documents — HTML

*1 week · 6 hours*

Write markup that means something. Structure first, appearance later: a heading is a heading because of what it is, not how it looks.

**HTML/CSS** · **Basic HTML** · **HTML5** · **W3C Consortium (World Wide Web Consortium)**

**Practice.** Mark up a two-page CV with no CSS at all. It must still be readable and correctly ordered with styling disabled.

### 3. Presentation — CSS

*2 weeks · 12 hours*

Lay out a page with the tools designed for layout, rather than fighting floats. Grid and container queries are the modern default; a utility or component framework is a choice made on top of understanding them.

**CSS3** · **CSS Grid Layout** · **Container Queries** · **SCSS (Sassy CSS)** · **Bootstrap** · **Tailwind CSS**

**Practice.** Rebuild the CV as a responsive two-column layout with CSS Grid, then make one component respond to its own width rather than the viewport's.

### 4. Programming the page

*2 weeks · 14 hours*

Manipulate the document from JavaScript, and understand why the library that once made this bearable is now largely unnecessary.

**JavaScript** · **ES6+ features** · **DOM Manipulation** · **jQuery** *(legacy)*

**Practice.** Add client-side form validation with no library. Then read a jQuery snippet from an old tutorial and write down its modern equivalent.

### 5. Modules, types and tooling

*1 week · 7 hours*

Move from script tags to a real build. Understand what a bundler does before adopting one, so its failure modes are diagnosable.

**ES Modules (ESM)** · **Import Maps** · **TypeScript** · **Vite** · **esbuild** · **Minification**

**Practice.** Convert the project to ES modules, add a Vite build, then compare the development and production output byte for byte.

### 6. Component frameworks

*2 weeks · 14 hours*

Learn one framework properly and recognise the family resemblance in the rest. Note that Angular and AngularJS are different projects — the second was retired in 2010 and is not a version of the first.

**Frameworks and Libraries** · **React.js** · **Vue.js** · **Svelte** · **Angular** · **AngularJS** *(legacy)* · **SPAs (Single Page Applications)** · **Hydration**

**Practice.** Rebuild one page as components in a framework of your choice, and write a paragraph on what the framework saved you and what it cost you.

### 7. Fast and findable

*1 week · 6 hours*

Performance is measurable, so measure it. Core Web Vitals are the metrics that search engines actually use, which makes speed and discoverability the same conversation.

**Core Web Vitals** · **LCP (Largest Contentful Paint)** · **INP (Interaction to Next Paint)** · **CLS (Cumulative Layout Shift)** · **Caching** · **SEO**

**Practice.** Measure the three vitals on your own site, make one change to improve the worst of them, and measure again.

### 8. Front-end security

*1 week · 6 hours*

Understand each defence as an answer to a specific attack, not as a configuration ritual. CSP exists because of XSS; CORS exists because the same-origin policy would otherwise be too strict to be usable.

**Threats** · **XSS (Cross-Site Scripting)** · **CSRF (Cross-Site Request Forgery)** · **CSP (Content Security Policy)** · **CORS (Cross-Origin Resource Sharing)** · **TLS / HTTPS**

**Practice.** Introduce a deliberate XSS hole in a local copy, exploit it, then close it with a Content Security Policy and confirm the exploit stops working.

### 9. Publishing

*1 week · 6 hours*

Get it onto the public web, under version control, in a way you can repeat tomorrow without remembering anything.

**Git** · **GitHub** · **Static Web Pages** · **JAMStack** · **Progressive Web Apps (PWAs)** · **Service Workers**

**Practice.** Deploy the site from a Git repository, then make it load once offline with a service worker.

---

## Back-End with Python

`intermediate` · 14 weeks · 86 hours · about 6 h/week

The server side of the same round trip: data modelling, two Python frameworks at different points on the batteries-included axis, APIs, the attacks that target them, and getting the result to run somewhere other than your laptop.

**Who it is for.** Students who have completed Front-End Foundations, or who can already build a static site and read JavaScript.

**By the end.** You can design a relational schema, expose it through a documented HTTP API, defend it against the standard attack classes, and deploy it in a container.

**Prerequisites.** [Front-End Foundations](#front-end-foundations)

### 1. Programming foundations

*1 week · 6 hours*

Establish the vocabulary the rest of the path assumes. A paradigm is a way of organising a program, not a language feature.

**Programming** · **Paradigms** · **OOP (Object-Oriented Programming)** · **Algorithmic**

**Practice.** Take one procedural script you have written and restructure it around objects. Note honestly which parts got clearer and which got longer.

### 2. Server-side basics

*1 week · 6 hours*

Understand what a server process is and what it is doing between requests, before a framework hides it.

**Server-Side Programming** · **Server** · **Python/PHP** · **Python**

**Practice.** Serve a page from a Python standard-library HTTP server, with no framework at all, and handle one POST by hand.

### 3. Relational data

*2 weeks · 12 hours*

Model data as relations and query it directly. SQL first, so the ORM later is a convenience rather than a mystery.

**Databases** · **Databases** · **SQL**

**Practice.** Design a schema for a small library catalogue and answer five questions about it in raw SQL, including one join and one aggregate.

### 4. When relational is the wrong shape

*1 week · 6 hours*

Recognise the workloads that relational tables serve badly, and what each alternative family trades away to serve them better.

**NoSQL** · **Graph Databases** · **Vector Databases** · **Big Data**

**Practice.** Take the catalogue schema and write down what a graph store would make easy that SQL makes awkward — and what you would lose.

### 5. A small framework — Flask

*2 weeks · 12 hours*

Build a web application from explicit parts, where every piece of routing, templating and configuration is something you wrote.

**Web Frameworks** · **Flask** · **MVC** · **Templating Engines**

**Practice.** Build a CRUD interface over the catalogue with Flask and a template engine, with no ORM.

### 6. A batteries-included framework — Django

*2 weeks · 12 hours*

Contrast Flask's explicitness with a framework that makes the decisions for you, and see what an ORM buys and costs against the raw SQL you wrote.

**Django** · **ORM (Object-Relational Mapping)**

**Practice.** Rebuild the same catalogue in Django, then inspect the SQL its ORM actually emits for your three most common queries.

### 7. APIs

*2 weeks · 12 hours*

Expose the data to clients you do not control. REST is the default; know when a graph query language or a persistent socket fits better.

**Web Services and APIs** · **RESTful APIs** · **JSON** · **Data Exchange Formats** · **GraphQL** · **WebSockets**

**Practice.** Publish the catalogue as a JSON API, consume it from the front end you built in the previous path, and fix the CORS error you will get.

### 8. Securing it

*1 week · 7 hours*

Attack your own application. Every defence in this module answers a specific one of the threats listed beside it.

**Threats** · **SQL Injection** · **CSRF (Cross-Site Request Forgery)** · **Phishing** · **Defenses** · **TLS / HTTPS** · **WebAuthn and Passkeys**

**Practice.** Write a deliberately vulnerable query, exploit it with SQL injection, then fix it with parameter binding and confirm the exploit fails.

### 9. Running it somewhere else

*1 week · 7 hours*

Separate "works on my machine" from "works". Understand the ladder from a virtual machine to a managed platform to no server at all.

**Virtualization** · **Docker** · **Cloud Computing** · **IaaS (Infrastructure as a Service)** · **PaaS (Platform as a Service)** · **SaaS (Software as a Service)** · **Heroku** *(legacy)* · **Serverless Architecture**

**Practice.** Containerise the application, run it from the image on a clean machine, and list what the container still assumes about its environment.

### 10. Working like a team

*1 week · 6 hours*

The practices that make the previous nine modules survivable with other people involved.

**Software Engineering** · **Agile** · **Scrum** · **DevOps** · **Git** · **GitHub**

**Practice.** Put the project under version control with a branch per feature, and set up one automated check that runs on every push.

---

## Full Stack

`advanced` · 13 weeks · 85 hours · about 7 h/week

Joining the two halves: rendering strategies that span client and server, realtime transport, browser platform APIs, and a substantial block on ERP development with Odoo — the stack this course is taught around.

**Who it is for.** Students who have completed both Front-End Foundations and Back-End with Python, or who work across both already.

**By the end.** You can choose a rendering strategy and defend the choice, build against a real ERP framework, and take the result from a container to an orchestrated deployment.

**Prerequisites.** [Front-End Foundations](#front-end-foundations), [Back-End with Python](#back-end-with-python)

### 1. Where the work happens

*1 week · 7 hours*

The central full-stack question is not which framework but which machine does the rendering, and when. Everything downstream follows from that.

**MVC** · **Client-Side** · **Server-Side Programming** · **RESTful APIs**

**Practice.** Draw the request lifecycle for the same page rendered three ways: fully on the server, fully in the browser, and split between them.

### 2. Meta-frameworks

*2 weeks · 14 hours*

Frameworks that answer the previous module's question for you. Learn what each one has decided on your behalf.

**Meta-Frameworks** · **Next.js** · **Nuxt** · **SvelteKit** · **Remix** · **Astro** · **Hydration** · **JAMStack**

**Practice.** Build the same three-page app twice, in two different meta-frameworks, and compare the shipped JavaScript payload.

### 3. Realtime and streaming

*1 week · 7 hours*

Not every interaction fits request-and-response. Know the three transports and which problem each was built for.

**WebSockets** · **Streaming Responses** · **WebRTC**

**Practice.** Add a live-updating view over a WebSocket, then implement the same feature with polling and measure the difference in requests and latency.

### 4. The browser as a platform

*2 weeks · 12 hours*

Capabilities that used to require a native application: background code, offline storage, a component model without a framework, and near-native compute.

**Progressive Web Apps (PWAs)** · **Service Workers** · **Web Components** · **WebAssembly** · **WebGPU**

**Practice.** Make the app installable and usable offline, and write one custom element that works with no framework present.

### 5. ERP and the Odoo stack

*3 weeks · 21 hours*

A full-stack framework from a different tradition, where the data model is the application. Note that Odoo's OWL is the Odoo Web Library, unrelated to the Web Ontology Language of the semantic-web path.

**Information Systems** · **ERP Systems** · **Odoo Framework** · **ORM (Object-Relational Mapping)** · **OWL (Odoo Web Library)** · **Templating Engines** · **QWeb**

**Practice.** Build a small Odoo module with its own model, a QWeb view and an OWL component, and explain which of the three the ORM is driving.

### 6. Containers and orchestration

*2 weeks · 12 hours*

One container is a packaging decision; many containers is an architecture. Know where the boundary sits and what crossing it costs.

**Virtualization** · **Docker** · **Kubernetes** · **Serverless Architecture** · **Cloud Computing**

**Practice.** Compose the application and its database as two containers, then write down what you would have to solve before running three replicas.

### 7. Performance in production

*1 week · 6 hours*

The same metrics as the front-end path, now with a server, a database and a cache in the path — where most of the latency actually lives.

**Core Web Vitals** · **Caching** · **Minification** · **SEO**

**Practice.** Profile a slow page end to end and attribute the time to network, server, query and render. Fix whichever dominates.

### 8. Delivering as a team

*1 week · 6 hours*

Tooling and process for work that no longer fits in one person's head.

**Agile** · **Scrum** · **DevOps** · **Git** · **GitHub** · **IDEs (Integrated Development Environments)** · **VS Code** · **PyCharm**

**Practice.** Set up continuous integration that runs the test suite and refuses a merge when it fails.

---

## Semantic Web & Knowledge Graphs

`advanced` · 11 weeks · 66 hours · about 6 h/week

Web 3.0 as the W3C meant it: making data machine-readable through identifiers, RDF, ontologies and query. Ends where this material now meets language models, which is the live research question rather than a footnote.

**Who it is for.** Students with some web development behind them who want the data layer, and anyone approaching knowledge graphs from a database or AI direction.

**By the end.** You can model a domain in RDF, express constraints in an ontology, query it with SPARQL, and explain precisely how a knowledge graph and a vector index answer different questions about the same corpus.

**Prerequisites.** [Front-End Foundations](#front-end-foundations)

### 1. What Web 3.0 means here

*1 week · 5 hours*

Settle the terminology before it causes trouble. In this course Web 3.0 is the Semantic Web; "Web3" is a later and separate coinage from the cryptocurrency industry. Both appear in the literature you will read.

**Web3 vs Web 3.0 — a note on terminology** · **Static Web Pages** · **Dynamic and Interactive Web** · **Social Media Integration** · **Blockchain and Decentralization**

**Practice.** Find three articles using "Web3" and classify each by which of the two meanings the author intends. Some will not be decidable — say so.

### 2. Identity and encoding

*1 week · 6 hours*

Everything downstream is built on being able to name a thing unambiguously and write that name down. IRIs are what let those names leave ASCII.

**URI/URL** · **IRI (Internationalized Resource Identifier)** · **Data Encoding** · **Unicode** · **UTF-8** · **UTF-16** · **Unicode, Inc. (Unicode Consortium)**

**Practice.** Take ten entities from a domain you know and mint a URI for each. Justify why yours will still resolve in ten years, or admit that it will not.

### 3. Exchange formats

*1 week · 6 hours*

The serialisations RDF arrives in, and the tree-shaped formats it is usually confused with.

**Data Exchange Formats** · **XML** · **XPath (XML Path Language)** · **JSON** · **CSV (Comma-Separated Values)**

**Practice.** Express the same five facts as XML, as JSON and as a CSV table, then note which relationships each format cannot state without a convention.

### 4. RDF and linked data

*2 weeks · 12 hours*

The triple as the unit of meaning, and the four principles that make a collection of triples a web rather than a file.

**Linked Data** · **RDF/ RDFS** · **W3C Consortium (World Wide Web Consortium)**

**Practice.** Publish your ten entities as RDF, linking at least three of them to identifiers on an existing public dataset rather than inventing your own.

### 5. Ontologies and rules

*2 weeks · 12 hours*

Move from describing data to constraining it. What a reasoner can derive that was never explicitly written down is the whole point.

**OWL** · **SWRL/RIF**

**Practice.** Write an ontology for your domain with two class hierarchies and one property restriction, then run a reasoner and inspect what it inferred.

### 6. Querying graphs

*1 week · 7 hours*

SPARQL against RDF, set beside the SQL you already know. The comparison is the fastest way to see what graph query buys you.

**SPARQL** · **SQL** · **Graph Databases**

**Practice.** Write the same question as a SPARQL query and a SQL query over equivalent data, and compare what each needs you to know about the schema in advance.

### 7. Knowledge graphs in practice

*1 week · 6 hours*

What changes at scale, and why industrial knowledge graphs look different from the textbook version.

**Knowledge Graphs** · **Databases** · **Big Data**

**Practice.** Load a public knowledge graph extract and answer one question that would require three joins in a relational schema.

### 8. Where this meets language models

*2 weeks · 12 hours*

Embeddings retrieve by similarity; a knowledge graph answers by structure. Retrieval-augmented generation uses the first, and increasingly wants the second. Knowing which failure belongs to which is the useful skill.

**AI (Artificial Intelligence)** · **LLMs (Large Language Models)** · **NLP** · **Prompt Engineering** · **Embeddings** · **Vector Databases** · **RAG (Retrieval-Augmented Generation)** · **MCP (Model Context Protocol)** · **AI Agents**

**Practice.** Build a small RAG pipeline over your own documents, then find a question it answers wrongly and explain whether a graph would have got it right.

---
