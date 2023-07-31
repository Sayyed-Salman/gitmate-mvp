# Custom host and remote provider

If you have built yourself a new remote hosting solution that is not what the majoriy uses you can customize the api for your needs.
Create a new `provider` class that inherits from `Provider` and implement the methods you need.

## Development

- Create a new entry in `status.json` with feild `custom` set to `true`
- Create a new file `custom.json` store the host and url with the following details

```json
{
  "host": "mycustomhost",
  "url": "https://mycustomhost.com/api/v1"
}
```

- cli will push the code to the new host and url
