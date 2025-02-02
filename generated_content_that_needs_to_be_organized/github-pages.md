# GitHub Pages Setup for AI Academy Labs

## Directory Structure

```
docs/
├── _config.yml               # Jekyll configuration
├── _layouts/                 # Page templates
│   ├── default.html         # Main layout
│   ├── lesson.html         # Lesson layout
│   └── interactive.html    # Interactive demo layout
├── _includes/               # Reusable components
│   ├── header.html
│   ├── footer.html
│   ├── navigation.html
│   └── interactive-demo.html
├── assets/                  # Static resources
│   ├── css/
│   ├── js/
│   └── images/
├── index.md                # Home page
├── curriculum/             # Main content
│   ├── index.md           # Curriculum overview
│   └── modules/           # Learning modules
├── demos/                  # Interactive demonstrations
│   ├── index.md           # Demo directory
│   └── embedded/          # Embedded demos
└── resources/             # Additional materials
    └── index.md           # Resource directory
```

## _config.yml Configuration

```yaml
title: AI Academy Labs
description: Learn AI from First Principles
baseurl: "/ai-academy-labs"
url: "https://cogentecho.ai"

# Theme settings
theme: jekyll-theme-minimal
plugins:
  - jekyll-sitemap
  - jekyll-seo-tag

# Navigation
navigation:
  - title: Home
    url: /
  - title: Curriculum
    url: /curriculum/
  - title: Demos
    url: /demos/
  - title: Resources
    url: /resources/

# Defaults
defaults:
  - scope:
      path: ""
    values:
      layout: default
  - scope:
      path: "curriculum"
    values:
      layout: lesson
  - scope:
      path: "demos"
    values:
      layout: interactive
```

## Example Lesson Layout (_layouts/lesson.html)

```html
---
layout: default
---
<div class="lesson-container">
  <div class="lesson-navigation">
    {% include navigation.html %}
  </div>
  
  <article class="lesson-content">
    <h1>{{ page.title }}</h1>
    
    {% if page.prerequisites %}
    <div class="prerequisites">
      <h3>Prerequisites</h3>
      <ul>
      {% for prerequisite in page.prerequisites %}
        <li><a href="{{ prerequisite.url }}">{{ prerequisite.title }}</a></li>
      {% endfor %}
      </ul>
    </div>
    {% endif %}
    
    {{ content }}
    
    {% if page.interactive_demo %}
    <div class="interactive-demo">
      {% include interactive-demo.html demo=page.interactive_demo %}
    </div>
    {% endif %}
  </article>
  
  <div class="lesson-resources">
    {% if page.additional_resources %}
    <h3>Additional Resources</h3>
    <ul>
    {% for resource in page.additional_resources %}
      <li><a href="{{ resource.url }}">{{ resource.title }}</a></li>
    {% endfor %}
    </ul>
    {% endif %}
  </div>
</div>
```
