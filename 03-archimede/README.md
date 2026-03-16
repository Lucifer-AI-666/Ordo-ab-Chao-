# Archimede Private Agent

Agente progettista locale, esperto di GitHub e domini affini (GitLab, CI/CD, DevOps, architettura software, gestione progetti open-source).

## Caratteristiche principali

- **Intuizione progettuale**: quando chiedi un'idea — anche in modo vago — Archimede analizza il contesto e propone subito la soluzione più utile per il tuo progetto, spiegando perché.
- **Expertise GitHub completa**: Actions, Issues, Projects, Releases, branch strategy, PR workflow, Codespaces, Pages, Discussions.
- **CI/CD & DevOps**: pipeline YAML, build/test/deploy, secrets, caching, matrix builds.
- **Architettura software**: scelta stack, monorepo, microservizi, API design, sicurezza dipendenze.
- **Developer Experience**: Conventional Commits, linting, CHANGELOG automatici, semantic versioning, pre-commit hooks.
- **Documentazione**: ADR, wiki, Docusaurus, MkDocs, OpenAPI.

## Setup

```bash
cd 03-archimede
ollama create archimede_private -f ArchimedePrivateAgent.Modelfile
ollama run archimede_private
```

## Utilizzo

Fai domande dirette o vaghe — Archimede intuisce cosa serve:

```
> Ho un progetto Node.js appena iniziato, cosa faccio prima?

> Dammi un'idea per migliorare il repo

> Come struttura la CI per un monorepo Python/Go?
```

### Parametri modello

| Parametro     | Valore |
|---------------|--------|
| `temperature` | 0.5    |
| `top_k`       | 50     |
| `top_p`       | 0.9    |
| Base model    | mistral:7b-instruct |

## Formato risposta

Le risposte seguono sempre la struttura:
- **Idea** — la proposta concreta
- **Perché ora** — il valore immediato
- **Come iniziare** — passi d'azione (max 5)
- **Alternative** — opzioni secondarie se il contesto è ambiguo
