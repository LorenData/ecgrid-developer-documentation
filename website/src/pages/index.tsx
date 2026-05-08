// AI Attribution — Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: ECGrid branded homepage — replaces Docusaurus default - Greg Kolinski
// 2026-05-08: Logo-forward hero, ECGrid palette accents, Roboto Condensed - Greg Kolinski

import type { ReactNode } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

/* ------------------------------------------------------------------ */
/* Hero — logo as the focal point                                        */
/* ------------------------------------------------------------------ */

function Hero() {
  const logoSrc = useBaseUrl('/img/ecgrid-network.svg');
  return (
    <header className={styles.hero}>
      <div className={clsx('container', styles.heroInner)}>
        <div className={styles.heroLogoWrap}>
          <img src={logoSrc} alt="ECGrid" className={styles.heroLogoImg} />
        </div>
        <p className={styles.heroEyebrow}>ECGrid B2B Integration Platform</p>

        <Heading as="h1" className={styles.heroTitle}>
          API-first EDI.<br />Build without limits.
        </Heading>

        <p className={styles.heroSubtitle}>
          Connect your application to the global ECGrid B2B network — provision mailboxes,
          route any-to-any documents, and embed enterprise EDI directly into your platform.
          Available as a JSON REST API and a full-featured SOAP API.
        </p>

        <div className={styles.heroButtons}>
          <Link className="button button--primary button--lg" to="/docs/getting-started/platform-overview">
            Get Started
          </Link>
          <Link className="button button--outline button--lg" to="/docs/rest-api/overview">
            REST API Reference
          </Link>
          <Link className="button button--outline button--lg" to="/docs/soap-api/overview">
            SOAP API Reference
          </Link>
        </div>

        <p className={styles.heroBadge}>
          <span className={styles.activePill}>REST API v2.6 — Active</span>
          <span className={styles.legacyPill}>ECGridOS SOAP v4.1 — Established</span>
        </p>
      </div>

    </header>
  );
}

/* ------------------------------------------------------------------ */
/* API path cards                                                        */
/* ------------------------------------------------------------------ */

type ApiCardProps = {
  badge: string;
  badgeVariant: 'active' | 'legacy';
  title: string;
  description: string;
  bullets: string[];
  to: string;
  linkLabel: string;
};

function ApiCard({ badge, badgeVariant, title, description, bullets, to, linkLabel }: ApiCardProps): ReactNode {
  return (
    <div className={clsx('col col--6', styles.cardCol)}>
      <div className={clsx(
        styles.card,
        badgeVariant === 'active' ? styles.cardActive : styles.cardLegacy,
      )}>
        <span className={clsx(styles.badge, badgeVariant === 'legacy' && styles.badgeLegacy)}>
          {badge}
        </span>
        <Heading as="h3" className={styles.cardTitle}>{title}</Heading>
        <p className={styles.cardDesc}>{description}</p>
        <ul className={styles.cardBullets}>
          {bullets.map((b, i) => <li key={i}>{b}</li>)}
        </ul>
        <div className={styles.cardFooter}>
          <Link className="button button--primary button--sm" to={to}>{linkLabel}</Link>
        </div>
      </div>
    </div>
  );
}

const apiCards: ApiCardProps[] = [
  {
    badge: 'v2.6 — Active',
    badgeVariant: 'active',
    title: 'REST API',
    description: 'JSON over HTTPS, stateless, and callable from any language or platform. Actively developed with new features and endpoints.',
    bullets: [
      '121 endpoints across 16 resource groups',
      'Equivalent coverage to the SOAP API',
      'X-API-Key header or Bearer JWT authentication',
      'Base URL: rest.ecgrid.io',
    ],
    to: '/docs/rest-api/overview',
    linkLabel: 'REST API Reference →',
  },
  {
    badge: 'v4.1 — Established',
    badgeVariant: 'legacy',
    title: 'ECGridOS SOAP API',
    description: 'Full WSDL-based SOAP API with equivalent coverage across all platform resources. Stable and production-ready.',
    bullets: [
      '242 endpoints for fine grain control',
      'XML/SOAP over HTTPS',
      'SessionID authentication (Login / Logout)',
      'Base URL: os.ecgrid.io/v4.1/prod/ECGridOS.asmx',
    ],
    to: '/docs/soap-api/overview',
    linkLabel: 'SOAP API Reference →',
  },
];

/* ------------------------------------------------------------------ */
/* Capability cards                                                      */
/* ------------------------------------------------------------------ */

type CapabilityProps = {
  icon: string;
  title: string;
  description: string;
};

function CapabilityCard({ icon, title, description }: CapabilityProps): ReactNode {
  return (
    <div className={clsx('col col--4', styles.capCol)}>
      <div className={styles.capCard}>
        <span className={styles.capIcon}>{icon}</span>
        <strong className={styles.capTitle}>{title}</strong>
        <p className={styles.capDesc}>{description}</p>
      </div>
    </div>
  );
}

const capabilities: CapabilityProps[] = [
  {
    icon: '📦',
    title: 'Mailbox Management',
    description: 'Create, configure, and manage trading partner mailboxes programmatically. No support tickets, no waiting.',
  },
  {
    icon: '📡',
    title: 'Document Tracking',
    description: 'Track every interchange end-to-end. Eliminate blind spots with live status, delivery receipts, and event callbacks.',
  },
  {
    icon: '🔗',
    title: 'Protocol Support',
    description: 'AS2, SFTP, FTPS, OFTP, X.400, ebXML, and X12.56 VAN interconnects — unified behind a single API.',
  },
  {
    icon: '🔄',
    title: 'Format Flexibility',
    description: 'Route X12, EDIFACT, XML, JSON, and custom formats between trading partners without conversion constraints.',
  },
  {
    icon: '🏗️',
    title: 'Platform Integration',
    description: 'Brand the experience as your own. Embed provisioning, monitoring, and operations directly into your platform UI.',
  },
  {
    icon: '⚡',
    title: 'Automation',
    description: 'Define workflows triggered by document arrival, error conditions, or trading partner events via callbacks.',
  },
];

/* ------------------------------------------------------------------ */
/* Nav cards + quick links                                               */
/* ------------------------------------------------------------------ */

type NavCardProps = { title: string; description: string; to: string };

function NavCard({ title, description, to }: NavCardProps): ReactNode {
  return (
    <div className={clsx('col col--4', styles.navCardCol)}>
      <Link className={styles.navCard} to={to}>
        <strong>{title}</strong>
        <span>{description}</span>
      </Link>
    </div>
  );
}

const navCards: NavCardProps[] = [
  { title: 'Getting Started', description: 'Platform overview, API keys, and quick-start guides', to: '/docs/getting-started/platform-overview' },
  { title: 'Common Operations', description: 'Step-by-step workflows: poll, upload, download, onboard', to: '/docs/common-operations/overview' },
  { title: 'Code Samples', description: 'Six .NET 10 sample projects for REST and SOAP', to: '/docs/code-samples/overview' },
];

const quickLinks = [
  { label: 'Quick Start — REST', to: '/docs/getting-started/quick-start-rest' },
  { label: 'Quick Start — SOAP', to: '/docs/getting-started/quick-start-soap' },
  { label: 'Authentication & API Keys', to: '/docs/getting-started/authentication-api-keys' },
  { label: 'Poll Inbound Files', to: '/docs/common-operations/poll-inbound-files' },
  { label: 'Upload EDI Files', to: '/docs/common-operations/upload-a-file' },
  { label: 'Onboard a Trading Partner', to: '/docs/common-operations/onboard-trading-partner' },
  { label: 'ENUMs Reference', to: '/docs/appendix/enums' },
  { label: 'Error Codes', to: '/docs/appendix/error-codes' },
  { label: 'Migrate SOAP → REST', to: '/docs/guides/migrating-soap-to-rest' },
  { label: 'Swagger UI ↗', href: 'https://rest.ecgrid.io/swagger/index.html' },
];

/* ------------------------------------------------------------------ */
/* Page                                                                  */
/* ------------------------------------------------------------------ */

export default function Home(): ReactNode {
  return (
    <Layout
      title="ECGrid Developer Documentation Portal"
      description="API-first EDI. Connect your application to the entire ECGrid network. REST API v2.6 and ECGridOS SOAP API v4.1 documentation by Loren Data Corp.">
      <Hero />

      <main>
        {/* Choose your API */}
        <section className={styles.apiSection}>
          <div className="container">
            <Heading as="h2" className={styles.sectionHeading}>Choose Your API</Heading>
            <div className="row">
              {apiCards.map((card, i) => <ApiCard key={i} {...card} />)}
            </div>
          </div>
        </section>

        {/* Platform capabilities — Dark Navy panel */}
        <section className={styles.capSection}>
          <div className="container">
            <Heading as="h2" className={styles.sectionHeading}>Platform Capabilities</Heading>
            <p className={styles.sectionSub}>
              ECGrid functions as an API-first EDI communication switch serving ISVs, SaaS platforms, and integration providers.
            </p>
            <div className="row">
              {capabilities.map((cap, i) => <CapabilityCard key={i} {...cap} />)}
            </div>
          </div>
        </section>

        {/* Navigation */}
        <section className={styles.navSection}>
          <div className="container">
            <div className="row">
              {navCards.map((card, i) => <NavCard key={i} {...card} />)}
            </div>
          </div>
        </section>

        {/* Quick links — Dark Navy band */}
        <section className={styles.quickSection}>
          <div className="container">
            <Heading as="h2" className={styles.quickHeading}>Quick Links</Heading>
            <div className={styles.quickGrid}>
              {quickLinks.map((link, i) =>
                link.href ? (
                  <a key={i} href={link.href} target="_blank" rel="noopener noreferrer" className={styles.quickLink}>
                    {link.label}
                  </a>
                ) : (
                  <Link key={i} to={link.to!} className={styles.quickLink}>{link.label}</Link>
                )
              )}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
