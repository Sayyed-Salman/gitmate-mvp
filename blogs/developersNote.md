# D3velopers note

- In my opinion weak VMs will die installing dotnet for gcm, the better option is to use credential.store with a file on the disk to store credentials and then when you are done with the VM, you can delete the file.

- A paid feature could be a token manager with encrypted tokens with a password stored on cloud, so when you login with gitmate pro account you can store tokens with gitmate and then when you login with gitmate on another machine you can fetch the tokens and use them to login to git providers.

### Encrypting the token

- The token can be encrypted using a password and then stored on the cloud.
