"""Serialise the concept tree as SKOS.

The mind map is a taxonomy, so it maps onto SKOS almost directly. Publishing it
as RDF makes it queryable rather than merely readable -- which is the point of a
knowledge-graph teaching artifact being itself a knowledge graph.

Restricted links are omitted entirely: this is a public artifact.
"""

from __future__ import annotations

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import DCTERMS, SKOS

from .model import MindMap

BASE = "https://samrepository.github.io/Web_Technologies_MindMap/"

#: Vocabulary namespace, for this project's own predicates (``wt:status``).
WT = Namespace(f"{BASE}ns#")
#: One namespace per URI kind, so that every term is usable as a SPARQL
#: prefixed name. A single namespace with ``concept/<id>`` local parts would
#: put a slash inside the local name, which makes ``wtc:django`` unparseable
#: and the graph far more awkward to query than it needs to be.
CONCEPT = Namespace(f"{BASE}concept/")
SCHEME = Namespace(f"{BASE}scheme/")

TITLE = "Web Technologies Mind Map"
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"

#: Bind these when querying dist/webtech.ttl.
PREFIXES = {"wt": WT, "wtc": CONCEPT, "wts": SCHEME}


def concept_uri(ident: str) -> URIRef:
    return CONCEPT[ident]


def scheme_uri(ident: str) -> URIRef:
    return SCHEME[ident]


def render(mm: MindMap) -> str:
    g = Graph()
    g.bind("skos", SKOS)
    g.bind("dcterms", DCTERMS)
    for prefix, ns in PREFIXES.items():
        g.bind(prefix, ns)

    for section in mm.sections:
        scheme = scheme_uri(section.id)
        g.add((scheme, RDF.type, SKOS.ConceptScheme))
        g.add((scheme, DCTERMS.title, Literal(section.heading, lang="en")))
        g.add((scheme, DCTERMS.license, URIRef(LICENSE_URL)))
        if section.intro:
            g.add((scheme, RDFS.comment, Literal(section.intro, lang="en")))

    for c in sorted(mm.concepts.values(), key=lambda c: c.id):
        node = concept_uri(c.id)
        scheme = scheme_uri(c.section)

        g.add((node, RDF.type, SKOS.Concept))
        g.add((node, SKOS.prefLabel, Literal(c.label, lang="en")))
        g.add((node, SKOS.inScheme, scheme))
        if c.definition:
            g.add((node, SKOS.definition, Literal(c.definition, lang="en")))
        for alias in c.aliases:
            g.add((node, SKOS.altLabel, Literal(alias, lang="en")))

        if c.parent:
            g.add((node, SKOS.broader, concept_uri(c.parent)))
        else:
            g.add((scheme, SKOS.hasTopConcept, node))
            g.add((node, SKOS.topConceptOf, scheme))

        for ref in c.see_also:
            g.add((node, SKOS.related, concept_uri(ref)))

        if c.status:
            g.add((node, WT.status, Literal(c.status)))
        if c.level:
            g.add((node, WT.level, Literal(c.level)))

        # Public links only. A restricted link's URL never enters the graph.
        for ln in c.public_links:
            if ln.url:
                g.add((node, RDFS.seeAlso, URIRef(ln.url)))

    return g.serialize(format="turtle")
