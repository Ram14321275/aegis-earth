#!/bin/bash

git status

echo "Review staged changes before commit."

git add frontend backend docs infrastructure scripts

git commit -m "$1"

git push origin main
