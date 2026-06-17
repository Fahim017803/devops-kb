CREATE DATABASE IF NOT EXISTS devops_kb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE devops_kb;

CREATE TABLE IF NOT EXISTS categories (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(50)  NOT NULL UNIQUE,
    slug  VARCHAR(50)  NOT NULL UNIQUE,
    icon  VARCHAR(10)  DEFAULT '□'
);

CREATE TABLE IF NOT EXISTS articles (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    slug        VARCHAR(200) NOT NULL UNIQUE,
    excerpt     TEXT,
    content     LONGTEXT,
    level       ENUM('Beginner','Intermediate','Advanced') DEFAULT 'Beginner',
    read_time   INT DEFAULT 5,
    is_featured BOOLEAN DEFAULT FALSE,
    category_id INT NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Seed: Categories
INSERT IGNORE INTO categories (name, slug, icon) VALUES
('CI/CD',       'cicd',        '⬛'),
('Kubernetes',  'kubernetes',  '⬛'),
('Docker',      'docker',      '⬛'),
('Cloud / AWS', 'aws',         '⬛'),
('Security',    'security',    '🟥'),
('Monitoring',  'monitoring',  '⬛'),
('Linux',       'linux',       '⬛'),
('IaC / Terraform', 'iac',    '🟧');

-- Seed: Sample articles (matching your design screenshot)
INSERT IGNORE INTO articles (title, slug, excerpt, content, level, read_time, is_featured, category_id) VALUES
(
  'Building a production-grade CI/CD pipeline with GitHub Actions, Docker, and self-hosted runners',
  'production-cicd-github-actions',
  'A complete walkthrough of setting up parallel security scanning, staged deployments with manual approval gates, and automated rollback strategies.',
  '# Full content goes here...',
  'Intermediate', 12, TRUE,
  (SELECT id FROM categories WHERE slug='cicd')
),
(
  'Kubernetes on a budget: KinD on EC2',
  'kubernetes-kind-ec2',
  'Run a full K8s cluster on a single $5/month EC2 instance — no EKS costs needed for learning.',
  '# Full content goes here...',
  'Beginner', 8, TRUE,
  (SELECT id FROM categories WHERE slug='kubernetes')
),
(
  'DevSecOps: adding Trivy and OWASP ZAP to your pipeline',
  'devsecops-trivy-owasp-zap',
  'Shift security left by scanning images and live endpoints automatically on every push.',
  '# Full content goes here...',
  'Intermediate', 10, TRUE,
  (SELECT id FROM categories WHERE slug='security')
),
(
  'AWS EC2 for DevOps engineers: the essentials',
  'aws-ec2-devops-essentials',
  'Security groups, key pairs, instance types, and cost control — what actually matters.',
  '# Full content goes here...',
  'Beginner', 7, TRUE,
  (SELECT id FROM categories WHERE slug='aws')
),
(
  'Docker fundamentals: images, containers, and volumes explained',
  'docker-fundamentals',
  'Everything you need to containerize your first application from scratch.',
  '# Full content goes here...',
  'Beginner', 6, FALSE,
  (SELECT id FROM categories WHERE slug='docker')
),
(
  'Kubernetes deployments, services, and ingress — a practical guide',
  'kubernetes-deployments-services-ingress',
  'Write real manifests and understand what each field actually does.',
  '# Full content goes here...',
  'Intermediate', 9, FALSE,
  (SELECT id FROM categories WHERE slug='kubernetes')
),
(
  'Monitoring your infrastructure with Prometheus and Grafana',
  'prometheus-grafana-monitoring',
  'Set up dashboards, alerts, and metrics collection in under an hour.',
  '# Full content goes here...',
  'Intermediate', 8, FALSE,
  (SELECT id FROM categories WHERE slug='monitoring')
),
(
  'Secrets management in Kubernetes: avoid the common mistakes',
  'kubernetes-secrets-management',
  'Base64 is not encryption. Here is how to actually protect your secrets.',
  '# Full content goes here...',
  'Advanced', 11, FALSE,
  (SELECT id FROM categories WHERE slug='security')
),
(
  'AWS free tier survival guide: avoid surprise charges',
  'aws-free-tier-survival-guide',
  'The exact services and settings that lead to unexpected bills — and how to stay safe.',
  '# Full content goes here...',
  'Beginner', 5, FALSE,
  (SELECT id FROM categories WHERE slug='aws')
),
(
  'Infrastructure as Code with Terraform: from zero to production',
  'terraform-zero-to-production',
  'Provision, manage, and destroy cloud resources declaratively and repeatably.',
  '# Full content goes here...',
  'Advanced', 13, FALSE,
  (SELECT id FROM categories WHERE slug='iac')
);

-- Admin user table
CREATE TABLE IF NOT EXISTS admin_users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);
