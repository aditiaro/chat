# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

## Design

User --> Static Hosted Website on Azure - no charge - (Chat App)
--> First default message is displayed - No API call
--> User interacts with the Chat App
--> API Call to Lambda -- FastAPI Code - wraps langchain agents for GPT

## Pipeline

### Serverless stage
Stage 0: Tests - Unit/Integration (Mocking)
    tests/faas_demo
        - test_chat_response
Stage 1: Build a Azure Function docker container
Stage 2: Push docker container to registry (It will automatically update the Lambda)
Stage 4: Deploy - Cloud Stack - OPENAPI_KEY, env etc. 
Stage 5: E2E test running - python script

### Frontend stage
Stage 4: Test UI
Stage 5: Build UI - Webpack compiles your code into -> HTML, CSS, JS
Stage 6: Push to Azure Static website hosting
Stage 7: E2E - Selenium test

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)