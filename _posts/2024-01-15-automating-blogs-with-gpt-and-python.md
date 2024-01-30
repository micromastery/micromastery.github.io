---
title: Level up your Custom GPTs with GPT Actions
date: 2024-01-15 00:00:00 +0000
categories: [Blogging, Automation]
tags: [python, flask, github, oauth, gpt, jekyll, automation]
---

## Introduction

In today's fast-paced digital world, automation is key to efficiency. This blog post will guide you through setting up GPT actions with your own endpoint using python. As an example we will consider "Automating Blog Creation with Custom GPT Actions, Python Backend and Github pages". This setup allows for seamless integration with a GitHub repository using a Jekyll theme.

## Prerequisites

- A GitHub repository with a Jekyll theme.
- Basic knowledge of Python and Flask.
- A server for deploying the backend (options include Vercel, PythonAnywhere, etc.).

## Step 1: Setting Up the Python Backend

Our journey begins with setting up a Python backend using Flask. This backend will handle GitHub OAuth and posting markdown content to your repository.

```python
from flask import Flask, request, redirect
import requests
from urllib.parse import urlencode
import os
import base64

app = Flask(__name__)

CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('GITHUB_REDIRECT_URI')


# Endpoint to initiate GitHub OAuth flow
@app.route('/login')
def login():
    params = {'client_id': CLIENT_ID, 'redirect_uri': REDIRECT_URI, 'scope': 'repo'}
    url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    return redirect(url)

# Callback endpoint for GitHub OAuth
@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {'Accept': 'application/json'}
    response = requests.post('https://github.com/login/oauth/access_token', json=data, headers=headers)
    access_token = response.json().get('access_token')
    return access_token

# Endpoint to post markdown content to GitHub repo
@app.route('/post_markdown', methods=['POST'])
def post_markdown():
    access_token = request.headers.get('Authorization')
    if not access_token:
        return 'Access Token is required!', 401

    json_data = request.json
    file_name = json_data.get('file_name')
    content = json_data.get('content')

    repo = username/username.github.io'  # specify your repo
    path = f'_posts/{file_name}'  # specify the path inside your repo
    message = f'Add {file_name}'

    url = f'https://api.github.com/repos/{repo}/contents/{path}'
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'message': message,
        'content': base64.b64encode(content.encode()).decode(),
    }
    response = requests.put(url, json=data, headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
```

### Deploying the Backend

After writing the code, deploy it using your preferred platform. This enables the backend to be accessible via the internet.

## Step 2: GitHub Integration and Obtaining API Key

### Getting GitHub Client ID and Secret

Before integrating with GitHub, you need to obtain your client ID and client secret.

1. Go to your GitHub account settings.
2. Navigate to 'Developer settings' > 'OAuth Apps'.
3. Click on 'New OAuth App'.
4. Fill in the application name, homepage URL (can be the URL of your deployed backend), and Authorization callback URL (<deployed base url>/callback).
5. Once created, you will receive your client ID and secret.


### Using the Deployed Backend to Get API Key

Call `<url of your deployed backend>/login` to initiate the OAuth flow and obtain your API key.


## Step 3: Setting Up Custom GPT Actions

Now, let's integrate the backend with a custom GPT action.

### OpenAPI Schema Configuration

Configure the OpenAPI schema as follows to set up the action:

```yaml
{
  "openapi": "3.0.0",
  "info": {
    "title": "GitHub Integration API",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "<url of the deployed app>s"
    }
  ],
  "paths": {
    "/post_markdown": {
      "post": {
        "summary": "Post markdown content to GitHub repo",
        "operationId":"PostMarkDown",

        "responses": {
          "200": {
            "description": "Markdown content successfully posted",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "additionalProperties": true
                }
              }
            }
          },
          "401": {
            "description": "Unauthorized access"
          }
        },
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "file_name": {
                    "type": "string"
                  },
                  "content": {
                    "type": "string"
                  }
                },
                "required": ["file_name", "content"]
              }
            }
          }
        }
      }
    }
  }
}
```

### Setting Up Authentication

For the action setup, use "API Key" as the authentication type. Set the header name as "Authorization" and the value as the API key obtained earlier.

![Edit Actions](https://raw.githubusercontent.com/micromastery/micromastery.github.io/main/assets/Automated_Blog_Using_CustomGPT/Edit%20Actions.png)
![API Key Authentication Setup](https://raw.githubusercontent.com/micromastery/micromastery.github.io/main/assets/Automated_Blog_Using_CustomGPT/API%20Key%20Setup.png)

## Step 4: Writing and Posting Blogs

With everything set up, you can configure GPT as per your requirement to generate blogs and automate their posting to your GitHub repository.

## Conclusion

Automating blog creation with custom GPT actions and a Python backend is an efficient way to manage content. It streamlines the process, saving time and effort, and opens up new possibilities for content creators and developers alike.
