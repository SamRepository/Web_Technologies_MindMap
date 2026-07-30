<!-- GENERATED FILE -- do not edit.
     Source of truth: concepts/**/*.yml
     Regenerate with: python scripts/build.py -->

# Web Development

## Front-End Development

### HTML/CSS {#html-css}

- <span id="html5"></span>**HTML5**: The latest version of HTML, providing new elements, attributes, and behaviors.
  - [Official Documentation](https://www.w3.org/TR/html5/)
  - [Wikipedia](https://en.wikipedia.org/wiki/HTML5)

- <span id="css3"></span>**CSS3**: The latest evolution of the Cascading Style Sheets language, providing new features for layout, animation, and more.
  - [Official Documentation](https://www.w3.org/Style/CSS/)
  - [Wikipedia](https://en.wikipedia.org/wiki/CSS)
  - [YouTube Resource CS50](https://youtu.be/zFZrkCIc2Oc?si=IwtOYBIeU0pHk-Ht)

  - <span id="scss"></span>**SCSS (Sassy CSS)**: SCSS is a syntax of SASS (Syntactically Awesome Style Sheets), a CSS preprocessor that extends the capabilities of CSS. It allows developers to use variables, nested rules, mixins, and functions, making CSS more maintainable, reusable, and easier to write. SCSS is fully compatible with the original CSS syntax, making it a more powerful way to organize and streamline stylesheets in web development projects.
    - [Official Website](https://sass-lang.com/)
    - [Wikipedia](https://en.wikipedia.org/wiki/Sass_(stylesheet_language))

  - <span id="bootstrap"></span>**Bootstrap**: Bootstrap is a popular open-source front-end framework used for developing responsive and mobile-first websites. It provides a collection of HTML, CSS, and JavaScript components that simplify the development of web pages with a consistent layout and design. Bootstrap includes pre-designed components like navigation bars, buttons, forms, and grids, which allow developers to quickly build visually appealing and functional interfaces across different device sizes.
    - [Official Website](https://getbootstrap.com/)
    - [Wikipedia](https://en.wikipedia.org/wiki/Bootstrap_(front-end_framework))

  - <span id="tailwind-css"></span>**Tailwind CSS**: A utility-first CSS framework: instead of writing custom stylesheets, you compose small single-purpose classes directly in the markup. It takes the opposite approach to component frameworks like Bootstrap, trading readable HTML for the removal of the naming and dead-CSS problems that grow with a hand-written stylesheet.
    - [Official Website](https://tailwindcss.com/)
    - [Wikipedia](https://en.wikipedia.org/wiki/Tailwind_CSS)

  - <span id="css-grid"></span>**CSS Grid Layout**: A two-dimensional layout system that positions elements in rows and columns declared on the container. It replaced the float- and table-based hacks that page layout previously required, and complements Flexbox, which handles one dimension at a time.
    - [CSS Grid Layout Module](https://www.w3.org/TR/css-grid-1/)
    - [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout)

  - <span id="container-queries"></span>**Container Queries** `emerging`: Styling rules that respond to the size of a component's own container rather than the size of the viewport. This is what media queries could never express: a genuinely reusable component that adapts wherever it is placed, without knowing anything about the page around it.
    - [CSS Containment Module Level 3](https://www.w3.org/TR/css-contain-3/)
    - [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries)

### JavaScript {#javascript}

- <span id="es6-features"></span>**ES6+ features**: ECMAScript 6 (ES6) and later editions brought significant improvements to JavaScript, including new syntax and features.
  - [Official Documentation](https://www.ecma-international.org/publications-and-standards/standards/ecma-262/)
  - [Wikipedia](https://en.wikipedia.org/wiki/ECMAScript)

- <span id="dom-manipulation"></span>**DOM Manipulation**: The ability to interact with and update the Document Object Model (DOM) of a web page using JavaScript.
  - [Wikipedia](https://en.wikipedia.org/wiki/Document_Object_Model)
  - [YouTube Resource CS50](https://youtu.be/jrBhi8wbzPw?si=VBfKr147HqnytXIk)

- <span id="typescript"></span>**TypeScript**: A typed superset of JavaScript that compiles to plain JavaScript. Types are checked before the code runs and then erased, so TypeScript catches a whole class of errors at build time while shipping ordinary JavaScript to the browser. It is now the default choice for large front-end and Node codebases.
  - [Official Website](https://www.typescriptlang.org/)
  - [Wikipedia](https://en.wikipedia.org/wiki/TypeScript)

- <span id="esm"></span>**ES Modules (ESM)**: JavaScript's standard module system, using `import` and `export`. Browsers and Node both support it natively, which ended the long split between competing module formats such as CommonJS and AMD.
  - [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
  - [ECMAScript Modules](https://tc39.es/ecma262/#sec-modules)

  - <span id="import-maps"></span>**Import Maps** `emerging`: A JSON block in the page that tells the browser how to resolve bare module names such as `import 'lodash'` to real URLs. It allows a project to use named imports directly in the browser without a bundler rewriting them first.
    - [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/script/type/importmap)
    - [HTML Standard — import maps](https://html.spec.whatwg.org/multipage/webappapis.html#import-maps)

### Frameworks and Libraries {#frameworks-and-libraries}

- <span id="jquery"></span>**jQuery** `legacy`: A fast, small, and feature-rich JavaScript library that simplifies HTML DOM tree traversal and manipulation.
  - [Official Website](https://jquery.com/)
  - [Wikipedia](https://en.wikipedia.org/wiki/JQuery)

- <span id="react-js"></span>**React.js**: A JavaScript library for building user interfaces, maintained by Facebook and a community of developers.
  - [Official Website](https://reactjs.org/)
  - [Wikipedia](https://en.wikipedia.org/wiki/React_(JavaScript_library))

- <span id="angular"></span>**Angular**: A TypeScript-based framework for building dynamic web applications, developed by Google. Angular provides a complete solution out of the box, including routing, forms, HTTP client, and dependency injection.
  - [Official Website](https://angular.dev/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Angular_(web_framework))

- <span id="angularjs"></span>**AngularJS** `legacy`: The original JavaScript framework released by Google in 2010, superseded by Angular (above) and no longer maintained since January 2022. It is listed here because a large amount of older tutorial material still refers to it; note that AngularJS and Angular are distinct frameworks and are not compatible.
  - [Wikipedia](https://en.wikipedia.org/wiki/AngularJS)

- <span id="vue-js"></span>**Vue.js**: Vue.js is a progressive JavaScript framework used for building user interfaces and single-page applications. It is designed to be incrementally adoptable, meaning you can start with as little or as much of Vue as you like and scale up from there. Vue.js is known for its simplicity, flexibility, and ease of integration with other libraries or existing projects.
  - [Official Website](https://vuejs.org/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Vue.js)

- <span id="svelte"></span>**Svelte**: A UI framework that shifts most of its work to build time: components compile into direct DOM-updating JavaScript, so no framework runtime or virtual DOM ships to the browser.
  - [Official Website](https://svelte.dev/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Svelte)

- <span id="meta-frameworks"></span>**Meta-Frameworks**: Frameworks built on top of a UI library to supply what an application needs beyond rendering components: routing, data loading, server-side rendering, build configuration and deployment. They are where most production front-end work now starts.
  - [Wikipedia](https://en.wikipedia.org/wiki/Web_framework)

  - <span id="next-js"></span>**Next.js**: The most widely used React meta-framework, providing file-based routing, server-side and static rendering, and server components in one toolchain.
    - [Official Website](https://nextjs.org/)
    - [Wikipedia](https://en.wikipedia.org/wiki/Next.js)

  - <span id="nuxt"></span>**Nuxt**: The equivalent meta-framework for Vue, adding routing, rendering modes and a module ecosystem on top of Vue's component model.
    - [Official Website](https://nuxt.com/)

  - <span id="sveltekit"></span>**SvelteKit**: Svelte's official application framework, handling routing, data loading and the choice between server rendering, prerendering and client rendering per route.
    - [Official Documentation](https://svelte.dev/docs/kit/introduction)

  - <span id="remix"></span>**Remix**: A React framework built around web platform fundamentals — HTML forms, HTTP caching and nested routing — rather than around client-side state management.
    - [Official Website](https://remix.run/)

  - <span id="astro"></span>**Astro**: A framework aimed at content-heavy sites. It ships zero JavaScript by default and hydrates only the components you mark as interactive, and it can mix React, Vue and Svelte components in one project.
    - [Official Website](https://astro.build/)

- <span id="htmx"></span>**htmx**: A small library that lets HTML attributes issue AJAX requests and swap the returned HTML into the page. It deliberately inverts the single-page-app model: the server keeps rendering HTML, and very little application state lives in the browser.
  - [Official Website](https://htmx.org/)

### Browsers {#browsers}

Web browsers are software applications used to access, retrieve, and display content from the World Wide Web. Browsers interpret HTML, CSS, and JavaScript to render web pages and provide a user interface for interacting with online content. Popular browsers include Google Chrome, Mozilla Firefox, Microsoft Edge, and Safari.

- [Wikipedia](https://en.wikipedia.org/wiki/Web_browser)

- <span id="developer-mode"></span>**Developer Mode**: Developer Mode, or Developer Tools, is a set of tools provided by web browsers that allow developers to inspect and debug web applications directly in the browser. Developer Mode includes features like the Elements panel for inspecting HTML and CSS, the Console for running JavaScript, and the Network panel for analyzing HTTP requests.
  - [Wikipedia](https://en.wikipedia.org/wiki/Web_development_tools)
  - [MDN Web Docs - Browser Developer Tools](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_are_browser_developer_tools)

- <span id="client-side"></span>**Client-Side**: Client-side refers to operations that are performed by the client, which in most cases is the user's web browser. Client-side technologies include HTML, CSS, and JavaScript, which are executed on the user's device rather than on the server. This approach allows for dynamic user interfaces and interactive web experiences.
  - [Wikipedia](https://en.wikipedia.org/wiki/Client-side)

### Build Tooling {#build-tooling}

The programs that turn source files into what the browser actually loads: resolving modules, compiling TypeScript and JSX, bundling, minifying, and serving a fast development server with hot reloading.

- [Wikipedia](https://en.wikipedia.org/wiki/Build_automation)

- <span id="vite"></span>**Vite**: The de facto standard front-end build tool. In development it serves native ES modules so startup stays near-instant regardless of project size, and for production it bundles with Rollup.
  - [Official Website](https://vite.dev/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Vite_(software))

- <span id="esbuild"></span>**esbuild**: A JavaScript and TypeScript bundler written in Go, one to two orders of magnitude faster than the earlier JavaScript-based bundlers. Several other tools use it internally rather than reimplementing the work.
  - [Official Website](https://esbuild.github.io/)

## Back-End Development

### Server-Side Programming {#server-side-programming}

- <span id="oop"></span>**OOP (Object-Oriented Programming)**: OOP is a programming paradigm based on the concept of "objects," which are instances of classes. Objects can contain data in the form of fields (attributes or properties) and code in the form of methods (functions). OOP emphasizes principles such as encapsulation, inheritance, polymorphism, and abstraction, allowing for the creation of reusable and modular code. This paradigm is widely used in languages like Java, C++, Python, and JavaScript for building scalable and maintainable applications.
  - [Wikipedia](https://en.wikipedia.org/wiki/Object-oriented_programming)

- <span id="python-php"></span>**Python/PHP**

  - <span id="python"></span>**Python**: A versatile, high-level programming language widely used for web development, among other applications.
    - [Official Website](https://www.python.org/)
    - [Wikipedia](https://en.wikipedia.org/wiki/Python_(programming_language))
    - [YouTube Resource CS50](https://youtu.be/EOLPQdVj5Ac?si=ZenEOd-cywwXkpIE)

  - <span id="php"></span>**PHP**: A popular server-side scripting language designed for web development but also used as a general-purpose programming language.
    - [Official Website](https://www.php.net/)
    - [Wikipedia](https://en.wikipedia.org/wiki/PHP)

- <span id="node-js"></span>**Node.js**: A JavaScript runtime built on Chrome's V8 engine, designed for building scalable network applications.
  - [Official Website](https://nodejs.org/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Node.js)

- <span id="deno"></span>**Deno**: A JavaScript and TypeScript runtime from Node's original creator, addressing design regrets in Node: TypeScript runs without a build step, and file, network and environment access are denied unless explicitly granted.
  - [Official Website](https://deno.com/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Deno_(software))

- <span id="bun"></span>**Bun**: A JavaScript runtime built on JavaScriptCore that also bundles a package manager, test runner and bundler into one binary, competing with Node primarily on startup and install speed.
  - [Official Website](https://bun.sh/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Bun_(software))

### Databases {#databases-2}

- <span id="sql"></span>**SQL**: Structured Query Language (SQL) is a standardized language for managing and manipulating relational databases.
  - [Wikipedia](https://en.wikipedia.org/wiki/SQL)
  - [YouTube Resource CS50](https://youtu.be/YzP164YANAU?si=HygcU6En3Zr4NgB2)

- <span id="nosql"></span>**NoSQL**: A class of database management systems that do not follow all the rules of a relational database; it is often used for large-scale data storage.
  - [Wikipedia](https://en.wikipedia.org/wiki/NoSQL)

- <span id="graph-databases"></span>**Graph Databases**: A graph database is a type of NoSQL database that uses graph structures with nodes, edges, and properties to represent and store data. It is optimized for handling data with complex relationships and is particularly useful in applications like social networks, recommendation engines, and fraud detection. Nodes represent entities, while edges represent the relationships between those entities, making querying and navigating complex interconnected data efficient.
  - [Wikipedia](https://en.wikipedia.org/wiki/Graph_database)

- <span id="vector-databases"></span>**Vector Databases**: Vector databases are specialized databases designed to store, index, and query high-dimensional vectors. These databases are crucial for machine learning applications, particularly for similarity search, where the goal is to find vectors that are most similar to a given query vector. Vector databases are used in contexts such as recommendation systems, natural language processing, and computer vision.
  - [Wikipedia](https://en.wikipedia.org/wiki/Vector_space_model)

- <span id="big-data"></span>**Big Data**: Refers to extremely large data sets that require advanced tools and techniques to process and analyze. It is characterized by its volume, variety (types of data), velocity (speed of processing), and veracity (data accuracy). Big Data is used to uncover insights and patterns in fields like finance, healthcare, and social media.
  - [Wikipedia](https://en.wikipedia.org/wiki/Big_data)

### Web Frameworks {#web-frameworks}

- <span id="flask"></span>**Flask**: A lightweight WSGI web application framework in Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.
  - [Official Website](https://flask.palletsprojects.com/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Flask_(web_framework))
  - [Training Course - Pluralsight Path](https://drive.google.com/drive/folders/1ZGhmS15qIsTIGGgA5kFigI7AawwHx3Ga)

- <span id="django"></span>**Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
  - [Official Website](https://www.djangoproject.com/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Django_(web_framework))
  - [YouTube Resource CS50](https://youtu.be/w8q0C-C1js4?si=fFhDvSuZkNwZK5IO)
  - [Training Course - Pluralsight Path](https://drive.google.com/drive/folders/1tvsKwBmeNwwegdx5YJQGvzZnEK-GKZnx)

### Web Services and APIs {#web-services-and-apis}

- <span id="websockets"></span>**WebSockets**: A protocol that provides full-duplex communication channels over a single TCP connection, primarily used for real-time applications.
  - [Wikipedia](https://en.wikipedia.org/wiki/WebSocket)

- <span id="restful-apis"></span>**RESTful APIs**: Representational State Transfer (REST) is an architectural style for designing networked applications, allowing communication between client and server.
  - [Wikipedia](https://en.wikipedia.org/wiki/Representational_state_transfer)

## Full Stack Development

### Odoo Framework {#odoo-framework}

An open-source suite of business applications, including CRM, e-commerce, billing, accounting, manufacturing, warehouse, project management, and inventory management.

- [Official Website](https://www.odoo.com/)
- [Wikipedia](https://en.wikipedia.org/wiki/Odoo)

- <span id="erp-systems"></span>**ERP Systems**: Enterprise Resource Planning (ERP) systems are integrated management systems that allow organizations to manage business processes in a centralized system.
  - [Wikipedia](https://en.wikipedia.org/wiki/Enterprise_resource_planning)

- <span id="mvc"></span>**MVC**: Model-View-Controller (MVC) is a design pattern used for developing web applications. It divides an application into three interconnected components.
  - [Wikipedia](https://en.wikipedia.org/wiki/Model–view–controller)

- <span id="orm"></span>**ORM (Object-Relational Mapping)**: ORM is a programming technique that allows developers to interact with a relational database using the object-oriented paradigm. In ORM, objects in a programming language are mapped to database tables, and relationships between objects are managed through associations in the code rather than direct SQL queries. ORMs help simplify database interactions, improve code maintainability, and provide abstraction from the underlying database structure. Popular ORM frameworks include Hibernate for Java, Django ORM for Python, and Sequelize for Node.js.
  - [Wikipedia](https://en.wikipedia.org/wiki/Object-relational_mapping)

- <span id="owl-odoo-web-library"></span>**OWL (Odoo Web Library)**: Odoo's own component framework, used to build the web client interface. Not to be confused with OWL the Web Ontology Language, a W3C semantic web standard that shares the acronym but is unrelated.
  - [Odoo Documentation](https://www.odoo.com/documentation/15.0/developer/reference/addons/orm.html)

- <span id="templating-engines"></span>**Templating Engines**

  - <span id="qweb"></span>**QWeb**: A template engine in Odoo used to generate XML/HTML from model data. It allows for the creation of dynamic content in Odoo applications, supporting the rendering of reports, views, and other templates.
    - [Odoo Documentation](https://www.odoo.com/documentation/15.0/developer/reference/addons/qweb.html)

### IDEs (Integrated Development Environments) {#ides}

- <span id="vs-code"></span>**VS Code**: Visual Studio Code (VS Code) is a free, open-source code editor developed by Microsoft. It offers support for debugging, embedded Git control, syntax highlighting, intelligent code completion, snippets, and code refactoring.
  - [Official Website](https://code.visualstudio.com/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Visual_Studio_Code)

- <span id="pycharm"></span>**PyCharm**: PyCharm is a dedicated Python IDE developed by JetBrains. It provides essential tools for productive Python development, including code analysis, a graphical debugger, an integrated unit tester, and integration with version control systems.
  - [Official Website](https://www.jetbrains.com/pycharm/)
  - [Wikipedia](https://en.wikipedia.org/wiki/PyCharm)

## Web Security

### Threats {#threats}

Refer to the various vulnerabilities and attacks that can compromise the security of web applications, systems, and user data. These threats can exploit weaknesses in software, hardware, or human behavior, leading to unauthorized access, data breaches, or service disruptions. Some common web security threats include:

- <span id="xss"></span>**XSS (Cross-Site Scripting)**: An attack where malicious scripts are injected into trusted websites, enabling attackers to steal user data or hijack user sessions.
  - [Wikipedia](https://en.wikipedia.org/wiki/Cross-site_scripting)

- <span id="sql-injection"></span>**SQL Injection**: A code injection technique that exploits vulnerabilities in web applications by inserting malicious SQL queries, allowing attackers to access, modify, or delete database data.
  - [Wikipedia](https://en.wikipedia.org/wiki/SQL_injection)

- <span id="csrf"></span>**CSRF (Cross-Site Request Forgery)**: A type of attack where a malicious website tricks a user's browser into performing actions on another site without their consent, leading to unauthorized transactions or data changes.
  - [Wikipedia](https://en.wikipedia.org/wiki/Cross-site_request_forgery)

- <span id="ddos"></span>**DDoS (Distributed Denial of Service)**: An attack that overwhelms a website or server with a flood of internet traffic from multiple sources, making it unavailable to legitimate users.
  - [Wikipedia](https://en.wikipedia.org/wiki/Denial-of-service_attack)

- <span id="phishing"></span>**Phishing**: A type of social engineering attack where attackers disguise themselves as trustworthy entities to steal sensitive information like usernames, passwords, or credit card details.
  - [Wikipedia](https://en.wikipedia.org/wiki/Phishing)

### Defenses {#defenses}

The mechanisms that protect against the threats above. Security on the web is layered: transport encryption, strong authentication, and browser-enforced policies that limit what a page is permitted to load or reach.

- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)

- <span id="tls-https"></span>**TLS / HTTPS**: Transport Layer Security encrypts and authenticates the connection between browser and server, so traffic cannot be read or altered in transit. HTTPS is HTTP carried over TLS, and is now a prerequisite for most browser features.
  - [RFC 8446 (TLS 1.3)](https://datatracker.ietf.org/doc/html/rfc8446)
  - [Wikipedia](https://en.wikipedia.org/wiki/Transport_Layer_Security)

- <span id="webauthn-passkeys"></span>**WebAuthn and Passkeys**: A standard for signing in with public-key cryptography instead of a shared secret. The private key never leaves the user's device, so there is no password for a site to leak or an attacker to phish. Passkeys are WebAuthn credentials synchronised across a user's devices.
  - [Web Authentication Level 2](https://www.w3.org/TR/webauthn-2/)
  - [passkeys.dev](https://passkeys.dev/)
  - [Wikipedia](https://en.wikipedia.org/wiki/WebAuthn)

- <span id="content-security-policy"></span>**CSP (Content Security Policy)**: An HTTP header by which a page declares which sources it may load scripts, styles and other resources from. The browser enforces it, which turns most cross-site scripting from a full compromise into a blocked request.
  - [CSP Level 3](https://www.w3.org/TR/CSP3/)
  - [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)

- <span id="cors"></span>**CORS (Cross-Origin Resource Sharing)**: The mechanism by which a server opts in to being read by pages from other origins. It relaxes the same-origin policy in a controlled way; it is a permission system, not a restriction imposed on the server.
  - [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)
  - [Wikipedia](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)
