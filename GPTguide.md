### Backend (FastAPI - Python)

1. Install the necessary libraries:

   ```bash
   pip install fastapi uvicorn
   ```

2. Create a file named `main.py`:

   ```python
   from fastapi import FastAPI, HTTPException
   from fastapi.staticfiles import StaticFiles
   from pydantic import BaseModel

   app = FastAPI()

   app.mount("/", StaticFiles(directory="static", html=True), name="static")

   class Message(BaseModel):
       sender: str
       content: str

   messages = []

   @app.post("/send-message")
   def send_message(message: Message):
       messages.append(message)
       return {"status": "Message sent successfully"}

   @app.get("/get-messages")
   def get_messages():
       return messages
   ```

   This code sets up a FastAPI application with two endpoints - one for sending messages (`/send-message`) and one for retrieving messages (`/get-messages`). It also mounts the `static` folder to serve static files.

### Frontend (React with TypeScript)

1. Create a React app using Create React App:

   ```bash
   npx create-react-app react-chat-app --template typescript
   cd react-chat-app
   ```

2. Replace the contents of `src/App.tsx` with the following code:

   ```tsx
   import React, { useState, useEffect } from 'react';
   import { MessageList, Input } from 'react-chat-elements';
   import 'react-chat-elements/dist/main.css';

   const App: React.FC = () => {
     const [messages, setMessages] = useState<any[]>([]);
     const [input, setInput] = useState<string>('');

     const fetchMessages = async () => {
       const response = await fetch('/get-messages');
       const data = await response.json();
       setMessages(data);
     };

     useEffect(() => {
       fetchMessages();
     }, []);

     const handleSend = async () => {
       if (input.trim() !== '') {
         const response = await fetch('/send-message', {
           method: 'POST',
           headers: {
             'Content-Type': 'application/json',
           },
           body: JSON.stringify({
             sender: 'JohnDoe', // Replace with the appropriate username or implement user authentication
             content: input,
           }),
         });
         const data = await response.json();
         console.log(data);
         fetchMessages(); // Update messages after sending a new message
         setInput('');
       }
     };

     return (
       <div>
         <MessageList
           className="message-list"
           lockable={true}
           toBottomHeight={'100%'}
           dataSource={messages.map((message, index) => ({
             position: message.sender === 'JohnDoe' ? 'right' : 'left',
             type: 'text',
             text: message.content,
             date: new Date(),
             dateString: new Date().toLocaleTimeString(),
           }))}
         />
         <Input
           placeholder="Type here..."
           multiline={false}
           value={input}
           onChange={(e: any) => setInput(e.target.value)}
           rightButtons={[
             {
               color: 'black',
               text: 'Send',
               callback: () => handleSend(),
             },
           ]}
         />
       </div>
     );
   };

   export default App;
   ```

   This code sets up a simple React component that uses the `react-chat-elements` library for displaying messages and sending new messages through a REST API.

### Building and Deploying with GitHub Actions

Create a `.github/workflows/main.yml` file for the GitHub Actions workflow:

```yaml
name: Build and Deploy

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Install dependencies and build React app
      run: |
        cd react-chat-app
        npm install
        npm run build
      working-directory: ./react-chat-app

  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Deploy FastAPI and React app
      run: |
        cp -r react-chat-app/build/ static/
        uvicorn main:app --reload
      env:
        UVICORN_CMD: "uvicorn"
        FASTAPI_APP: "main:app"
```

This GitHub Actions workflow performs the following steps:
1. Checks out the code.
2. Installs dependencies and builds the React app.
3. Copies the React app build to the FastAPI static folder.
4. Starts the FastAPI server with UVicorn.

Make sure to adapt the workflow according to your project structure and requirements.

### Running the App Locally

1. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

2. Visit `http://localhost:8000` in your browser to see the chat application in action.

This example provides a basic setup for a FastAPI chat app with a REST API and a React frontend, and it includes a GitHub Actions workflow for building and deploying the app. Remember to enhance the security features and add more functionalities based on your specific requirements.

Certainly! Below is an example of an Azure Pipeline that deploys a React app to Azure Static Website hosting on Azure Storage and deploys a FastAPI backend as an Azure Function. The pipeline also addresses CORS issues by configuring CORS settings in the FastAPI app.

Create a file named `azure-pipelines.yml` at the root of your project:

```yaml
trigger:
- main

pr:
- main

variables:
  AZURE_STORAGE_ACCOUNT_NAME: '<your-storage-account-name>'
  AZURE_FUNCTION_APP_NAME: '<your-function-app-name>'
  AZURE_REGION: '<your-azure-region>'
  FRONTEND_APP_DIR: 'react-ui-app'  # Change this to your React app directory

jobs:
- job: BuildAndDeploy
  pool:
    vmImage: 'windows-latest'

  steps:
  - task: UseNode@1
    inputs:
      versionSpec: '14.x'
      checkLatest: true

  - script: |
      cd $(FRONTEND_APP_DIR)
      npm install
      npm run build
    displayName: 'Build React App'

  - task: PublishBuildArtifacts@1
    inputs:
      pathtoPublish: '$(FRONTEND_APP_DIR)/build'
      artifactName: 'frontend-artifact'
      publishLocation: 'Container'
    displayName: 'Publish Frontend Artifacts'

- job: DeployBackend
  pool:
    vmImage: 'windows-latest'

  steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.x'

  - script: |
      pip install azure-functions
      pip install azure-cli
    displayName: 'Install Azure Functions tools'

  - task: DownloadBuildArtifacts@0
    inputs:
      buildType: 'current'
      downloadType: 'single'
      artifactName: 'frontend-artifact'
      downloadPath: '$(Build.ArtifactStagingDirectory)'
    displayName: 'Download Frontend Artifacts'

  - task: AzureFunctionApp@1
    inputs:
      azureSubscription: '<your-azure-subscription>'
      appName: '$(AZURE_FUNCTION_APP_NAME)'
      package: '$(System.ArtifactsDirectory)/frontend-artifact'
      runtimeStack: 'python'
      runtimeVersion: '3.8'
    displayName: 'Deploy to Azure Function App'

- job: DeployFrontend
  pool:
    vmImage: 'windows-latest'

  steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.x'

  - task: AzureCLI@2
    inputs:
      azureSubscription: '<your-azure-subscription>'
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        # Get the storage account key
        accountKey=$(az storage account keys list --resource-group $(AZURE_STORAGE_ACCOUNT_NAME) --account-name $(AZURE_STORAGE_ACCOUNT_NAME) --query "[0].value" --output tsv)

        # Upload the frontend build to Azure Storage
        az storage blob upload-batch --account-name $(AZURE_STORAGE_ACCOUNT_NAME) --account-key $accountKey --destination '$web' --source '$(System.ArtifactsDirectory)/frontend-artifact'

    displayName: 'Deploy Frontend to Azure Storage'

  - task: AzureCLI@2
    inputs:
      azureSubscription: '<your-azure-subscription>'
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        # Get the storage account key
        accountKey=$(az storage account keys list --resource-group $(AZURE_STORAGE_ACCOUNT_NAME) --account-name $(AZURE_STORAGE_ACCOUNT_NAME) --query "[0].value" --output tsv)

        # Configure CORS for the storage account
        az storage cors add --account-name $(AZURE_STORAGE_ACCOUNT_NAME) --account-key $accountKey --origins '*' --methods GET POST OPTIONS --allowed-headers '*'

    displayName: 'Configure CORS for Azure Storage'

# Add necessary steps to configure CORS in your FastAPI app. 
# It might involve modifying the FastAPI app code or adding an Azure API Management instance.
```

Replace the placeholders `<your-storage-account-name>`, `<your-function-app-name>`, `<your-azure-region>`, and `<your-azure-subscription>` with your specific values. Also, adjust the `FRONTEND_APP_DIR` variable if your React app is located in a different directory.

This pipeline consists of three jobs:
1. **BuildAndDeploy:** Builds the React app and publishes the artifacts.
2. **DeployBackend:** Downloads the frontend artifacts and deploys the FastAPI app as an Azure Function.
3. **DeployFrontend:** Uploads the frontend build to Azure Storage and configures CORS settings.

Note: The CORS configuration for the FastAPI app might involve additional steps based on your application's structure. It could include modifying the FastAPI code or setting up Azure API Management.

Make sure to configure your Azure subscription and storage account access in Azure DevOps Pipelines, and set up the necessary Azure resources (Azure Function App, Storage Account) before running the pipeline. Adjust the pipeline according to your specific requirements and project structure.
