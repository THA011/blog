"""Static site generator for the Prowriters101 copywriting blog.

Modules:
    config   -- load and validate config.yaml
    content  -- parse Markdown + YAML frontmatter into Page/Post objects
    renderer -- wrap the Jinja2 environment
    site     -- orchestrate a full build
"""
