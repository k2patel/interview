# Assumptions
 - Projects are created using saperate modules, creating bounderies from admin account and project level saperation and api access.
 - 

# Following can be integrated using ci/cd or ansible using variables through the account management.
```
gcloud init
gcloud config set project unqork-379417
gcloud iam service-accounts create unqork
gcloud projects add-iam-policy-binding unqork-379417 --member="serviceAccount:unqork@unqork-379417.iam.gserviceaccount.com" --role="roles/owner"
```

# For local execution could use
```
export GOOGLE_OAUTH_ACCESS_TOKEN=$(gcloud auth print-access-token)
```
**Note: 1 Hr. Validity**

# Here can be generated Saperate artificact for each account / workspace environment.. depending on setup.
```
gcloud iam service-accounts keys create cred.json --iam-account=unqork@unqork-379417.iam.gserviceaccount.com
```

# Setup api access
```
gcloud services enable container.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

# simply use the new service account for terraform
```
export GOOGLE_APPLICATION_CREDENTIALS="./cred.json"
```

# Simple guide 
 * Terraform module mostly uses the local with workspace variable and some variables from the env.
 * iteration offloaded to ansible, documents are located in `ansible` folder.
 * create / modify `locals.tf` variable `credential_location`, use relative path expect to be in side the module.
 * Credential can be converted the env. variable easily through the ansible runtime and github variable.



