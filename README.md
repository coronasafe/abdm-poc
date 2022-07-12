# ABDM POC
This is a proof of concept HRP (Health Repository Provider) implementation using Fast API (Python) which aims to be Ayushman Bharat Digital Mission compliant.

## Resources
- [HIP integration docs](https://sandbox.abdm.gov.in/docs/build_hip)
- [API flow docs](https://stupendous-yumberry-7d0.notion.site/HRP-API-Flow-5df57be17b4847b9bd3ee742d8bd2801)

## Getting started
- Setup environment variables:
```
clientId=<secret>
clientSecret=<secret>
```
- Installing requirements: `pip install -r requirements.txt`
- Start server `uvicorn app.main:app --reload`
