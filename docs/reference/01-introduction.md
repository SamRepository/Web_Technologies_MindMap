<!-- GENERATED FILE -- do not edit.
     Source of truth: concepts/**/*.yml
     Regenerate with: python scripts/build.py -->

# Introduction to Web Technologies

## Internet Basics

### Networking {#networking-2}

- <span id="devices"></span>**Devices**

  - <span id="pc-mobile"></span>**PC/Mobile**: Personal computers (PCs) and mobile devices (smartphones and tablets) are end-user devices used to access the internet and run applications. PCs typically offer more processing power and flexibility, while mobile devices provide portability and convenience.
    - [Wikipedia - PC](https://en.wikipedia.org/wiki/Personal_computer)
    - [Wikipedia - Mobile Devices](https://en.wikipedia.org/wiki/Mobile_device)
    - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AD%D8%A7%D8%B3%D9%88%D8%A8_%D8%B4%D8%AE%D8%B5%D9%8A)

  - <span id="server"></span>**Server**: A server is a computer or system that provides resources, data, services, or programs to other computers, known as clients, over a network. Servers are essential for hosting websites, applications, databases, and other online services.
    - [Wikipedia](https://en.wikipedia.org/wiki/Server_(computing))
    - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AE%D8%A7%D8%AF%D9%88%D9%85)

  - <span id="switch"></span>**Switch**: A network switch is a device that connects devices within a network by using packet switching to receive, process, and forward data to the destination device. Switches operate at the data link layer (Layer 2) of the OSI model.
    - [Wikipedia](https://en.wikipedia.org/wiki/Network_switch)
    - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%85%D8%A8%D8%AF%D9%84_%28%D8%B4%D8%A8%D9%83%D8%A7%D8%AA%29)

  - <span id="router"></span>**Router**: A router is a networking device that forwards data packets between computer networks, typically connected to at least two networks (e.g., LAN and WAN). Routers determine the best path for data to travel from source to destination.
    - [Wikipedia](https://en.wikipedia.org/wiki/Router_(computing))
    - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%85%D9%88%D8%AC%D9%87_%28%D8%B4%D8%A8%D9%83%D8%A7%D8%AA%29)

- <span id="protocols"></span>**Protocols**

  - <span id="tcp-ip"></span>**TCP/IP**: The foundational communication protocols of the internet, responsible for routing and ensuring data integrity across networks.
    - [Official Documentation](https://www.ietf.org/standards/rfcs/)
    - [Wikipedia](https://en.wikipedia.org/wiki/Internet_protocol_suite)
    - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AD%D8%B2%D9%85%D8%A9_%D8%A8%D8%B1%D9%88%D8%AA%D9%88%D9%83%D9%88%D9%84%D8%A7%D8%AA_%D8%A7%D9%84%D8%A5%D9%86%D8%AA%D8%B1%D9%86%D8%AA)

  - <span id="dns"></span>**DNS**: The Domain Name System (DNS) translates human-friendly domain names into IP addresses required for locating and identifying computer services and devices.
    - [Official Website](https://www.iana.org/domains/root)
    - [Wikipedia](https://en.wikipedia.org/wiki/Domain_Name_System)
    - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%86%D8%B8%D8%A7%D9%85_%D8%A3%D8%B3%D9%85%D8%A7%D8%A1_%D8%A7%D9%84%D9%86%D8%B7%D8%A7%D9%82%D8%A7%D8%AA)

  - <span id="http-https"></span>**HTTP/HTTPS**: Hypertext Transfer Protocol (HTTP) is the foundation of data communication on the World Wide Web, while HTTPS is the secure version using encryption.
    - [Official Documentation](https://www.w3.org/Protocols/)
    - [Wikipedia](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol)
    - [Training Course - Pluralsight](https://drive.google.com/drive/folders/1-08W2MmXEgds8Ayn1_mrFKK3JB0JtU1Y)
    - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%A8%D8%B1%D9%88%D8%AA%D9%88%D9%83%D9%88%D9%84_%D9%86%D9%82%D9%84_%D8%A7%D9%84%D9%86%D8%B5%D9%88%D8%B5_%D8%A7%D9%84%D8%AA%D8%B1%D8%A7%D8%A8%D8%B7%D9%8A%D8%A9)

    - <span id="http-2"></span>**HTTP/2**: A major revision of HTTP that keeps the same semantics but changes how messages travel: requests are multiplexed over a single connection and headers are compressed, removing the need for the workarounds sites used to hide HTTP/1.1's one-request-at-a-time behaviour.
      - [RFC 9113](https://httpwg.org/specs/rfc9113.html)
      - [Wikipedia](https://en.wikipedia.org/wiki/HTTP/2)
      - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%A8%D8%B1%D9%88%D8%AA%D9%88%D9%83%D9%88%D9%84_%D9%86%D9%82%D9%84_%D8%A7%D9%84%D9%86%D8%B5_%D8%A7%D9%84%D9%81%D8%A7%D8%A6%D9%82/2)

    - <span id="http-3"></span>**HTTP/3**: The current major version of HTTP, carried over QUIC instead of TCP. Because each stream is independent, a single lost packet no longer stalls every other request on the connection, which matters most on mobile and lossy networks.
      - [RFC 9114](https://httpwg.org/specs/rfc9114.html)
      - [Wikipedia](https://en.wikipedia.org/wiki/HTTP/3)

      - <span id="quic"></span>**QUIC**: A transport protocol built on UDP that provides the reliability, congestion control and encryption that TCP plus TLS provide, but with a faster handshake and independent streams. It is the transport underneath HTTP/3.
        - [RFC 9000](https://datatracker.ietf.org/doc/html/rfc9000)
        - [Wikipedia](https://en.wikipedia.org/wiki/QUIC)
        - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%83%D9%88%D9%8A%D9%83_%28%D8%B4%D8%A8%D9%83%D8%A7%D8%AA%29)

### Data Encoding {#data-encoding}

- <span id="unicode"></span>**Unicode**: A standard for consistent encoding, representation, and handling of text expressed in most of the world's writing systems.
  - [Official Website](https://home.unicode.org/)
  - [Wikipedia](https://en.wikipedia.org/wiki/Unicode)
  - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D8%AA%D8%B1%D9%85%D9%8A%D8%B2_%D8%A7%D9%84%D9%85%D9%88%D8%AD%D8%AF)

  - <span id="utf-8"></span>**UTF-8**: UTF-8 (Unicode Transformation Format - 8-bit) is a variable-width character encoding used for electronic communication. It can encode all possible characters (code points) in Unicode using one to four bytes. UTF-8 is backward-compatible with ASCII and is widely used on the web for text representation due to its efficiency in encoding common characters and its compatibility across different systems.
    - [Wikipedia](https://en.wikipedia.org/wiki/UTF-8)
    - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%B5%D9%8A%D8%BA%D8%A9_%D8%A7%D9%84%D8%AA%D8%AD%D9%88%D9%8A%D9%84_%D8%A7%D9%84%D9%85%D9%88%D8%AD%D8%AF-8)

  - <span id="utf-16"></span>**UTF-16**: UTF-16 (Unicode Transformation Format - 16-bit) is another character encoding used to encode Unicode characters. It uses either one or two 16-bit code units to encode characters. While UTF-16 is more efficient for encoding characters beyond the Basic Multilingual Plane (BMP), it is less commonly used than UTF-8 for web content.
    - [Wikipedia](https://en.wikipedia.org/wiki/UTF-16)
    - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%8A%D9%88_%D8%AA%D9%8A_%D8%A7%D9%81-16)

### Data Acces {#data-acces}

- <span id="uri-url"></span>**URI/URL**: Uniform Resource Identifier (URI) and Uniform Resource Locator (URL) are standardized methods to identify and locate resources on the web.
  - [Official Documentation](https://tools.ietf.org/html/rfc3986)
  - [Wikipedia](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)
  - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%85%D8%B9%D8%B1%D9%81_%D8%A7%D9%84%D9%85%D9%88%D8%A7%D8%B1%D8%AF_%D8%A7%D9%84%D9%85%D9%88%D8%AD%D8%AF)

- <span id="iri"></span>**IRI (Internationalized Resource Identifier)**: IRI is an extension of the Uniform Resource Identifier (URI) that allows for the inclusion of non-ASCII characters. IRIs enable the use of characters from multiple languages and scripts, such as accented letters, Chinese, Arabic, or Cyrillic, within web addresses. This provides a more inclusive and globally accessible format for resource identification on the internet. IRIs can be converted to URIs for backward compatibility with systems that only support ASCII characters.
  - [Official Documentation](https://www.w3.org/International/O-URL-and-ident.html)
  - [Wikipedia](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier)

### Data Exchange Formats {#data-exchange-formats}

- <span id="xml"></span>**XML**: Extensible Markup Language (XML) is a flexible way to create common information formats and share data across the internet.
  - [Official Documentation](https://www.w3.org/XML/)
  - [Wikipedia](https://en.wikipedia.org/wiki/XML)
  - [Training Course - LinkedIn](https://drive.google.com/drive/folders/12jb9iion-lCvHaJTKK7tKtvmKDJmjoOI)
  - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%84%D8%BA%D8%A9_%D8%A7%D9%84%D8%AA%D8%A3%D8%B4%D9%8A%D8%B1_%D8%A7%D9%84%D9%88%D8%B3%D9%88%D8%B9%D8%A9)

  - <span id="xpath"></span>**XPath (XML Path Language)**: XPath is a query language for selecting nodes from an XML document. It provides a way to navigate through elements and attributes in an XML document using a path-like syntax. XPath is widely used in conjunction with XSLT, XQuery, and other XML technologies to retrieve specific parts of XML data.
    - [W3C Documentation](https://www.w3.org/TR/xpath-31/)
    - [Wikipedia](https://en.wikipedia.org/wiki/XPath)
    - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%A5%D9%83%D8%B3%D8%A8%D8%A7%D8%AB)

- <span id="json"></span>**JSON**: JavaScript Object Notation (JSON) is a lightweight data-interchange format that is easy for humans to read and write, and easy for machines to parse and generate.
  - [Official Documentation](https://www.json.org/json-en.html)
  - [Wikipedia](https://en.wikipedia.org/wiki/JSON)
  - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/JSON)

- <span id="csv"></span>**CSV (Comma-Separated Values)**: CSV is a simple file format used to store tabular data, such as a spreadsheet or database. Each line in a CSV file corresponds to a record, and each field in the record is separated by a comma. CSV files are commonly used for data exchange between different systems and applications due to their simplicity and wide support.
  - [Wikipedia](https://en.wikipedia.org/wiki/Comma-separated_values)
  - [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%82%D9%8A%D9%85_%D9%85%D9%81%D8%B5%D9%88%D9%84%D8%A9_%D8%A8%D9%81%D9%88%D8%A7%D8%B5%D9%84)

## Standardizing Entities

### W3C Consortium (World Wide Web Consortium) {#w3c-consortium}

The World Wide Web Consortium (W3C) has central Role in Standardizing Web Technologiesis. W3C is an international community that develops open standards to ensure the long-term growth of the web. W3C is responsible for creating and maintaining many of the key standards used to build websites, including HTML, CSS, and XML, ensuring the interoperability and accessibility of web technologies.

- [Official Website](https://www.w3.org/)
- [Wikipedia](https://en.wikipedia.org/wiki/World_Wide_Web_Consortium)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%B1%D8%A7%D8%A8%D8%B7%D8%A9_%D8%A7%D9%84%D8%B4%D8%A8%D9%83%D8%A9_%D8%A7%D9%84%D8%B9%D8%A7%D9%84%D9%85%D9%8A%D8%A9)

### Unicode, Inc. (Unicode Consortium) {#unicode-inc}

Unicode, Inc., commonly known as the Unicode Consortium, is a non-profit organization that develops and maintains the Unicode Standard, a universal character encoding scheme for text representation across different platforms and devices. This standard is essential for enabling consistent text data interchange across the internet and other platforms.

- [Official Website](https://home.unicode.org/)
- [Wikipedia](https://en.wikipedia.org/wiki/Unicode_Consortium)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%AC%D9%85%D8%B9%D9%8A%D8%A9_%D8%A7%D9%84%D8%AA%D8%B1%D9%85%D9%8A%D8%B2_%D8%A7%D9%84%D9%85%D9%88%D8%AD%D8%AF)

### ISO (International Organization for Standardization) {#iso}

ISO is an independent, non-governmental international organization that develops and publishes a wide range of standards across various industries. These standards ensure quality, safety, efficiency, and interoperability for products, systems, and services. ISO standards are crucial in areas like technology, web development, and data management.

- [Official Website](https://www.iso.org/)
- [Wikipedia](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D9%85%D9%86%D8%B8%D9%85%D8%A9_%D8%A7%D9%84%D8%AF%D9%88%D9%84%D9%8A%D8%A9_%D9%84%D9%84%D9%85%D8%B9%D8%A7%D9%8A%D9%8A%D8%B1)

### IEEE (Institute of Electrical and Electronics Engineers) {#ieee}

IEEE is the world's largest technical professional organization focused on advancing technology. It is widely recognized for creating standards in a variety of areas such as computing, networking, and electronics. IEEE standards help ensure interoperability, innovation, and quality across numerous technologies.

- [Official Website](https://www.ieee.org/)
- [Wikipedia](https://en.wikipedia.org/wiki/Institute_of_Electrical_and_Electronics_Engineers)
- [Wikipedia (Ar)](https://ar.wikipedia.org/wiki/%D9%85%D8%B9%D9%87%D8%AF_%D9%85%D9%87%D9%86%D8%AF%D8%B3%D9%8A_%D8%A7%D9%84%D9%83%D9%87%D8%B1%D8%A8%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D8%A5%D9%84%D9%83%D8%AA%D8%B1%D9%88%D9%86%D9%8A%D8%A7%D8%AA)
