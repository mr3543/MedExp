#!/bin/bash

wget "https://storage.googleapis.com/kaggle-data-sets/75301/170322/bundle/archive.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1587765727&Signature=aO1e8Bq8Mu9TyQQVkHXxRHLWSZaalEHOKe%2FEMFJxlLMc3n0PUCBBP9j6gj8%2BpJ%2BDXxWtztlbzd0DSSBM5LjNP8TA7bultvOvaZr0MUFdz1Q2wZluNafATiNl0PZ2KLTgGJ7rghOYE91dQ5IbTv0p61fvYdZRMcSFBtjCdCo2v3%2BBvetuzYmEy6W5ZTkY2xuSMcGNzZ41RPX42ZBvt2eiSxRPKm5LNw83StkvDFBtd%2FwR9dW%2F57q%2FN%2FzJknSV%2BZ4bFIAdybRMkN7qne7v12r0G60tQDufCKEQGdz9ASgzboCMgiPAFnmg9TLoZsMwruExMKSqiB82eU8MtZIuo73N9A%3D%3D&response-content-disposition=attachment%3B+filename%3Dmedium-articles-with-content.zip" --no-check-certificate -O "medium-data.zip"

unzip -qq medium-data.zip
rm medium-data.zip
