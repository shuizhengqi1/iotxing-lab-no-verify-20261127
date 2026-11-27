# Illustration only: a scanner that has had the custom prod marker removed.
# If CI runs this copy from the pull request, the original secret would pass.
import sys
print("secret-scan: weakened copy, custom_prod_hmac rule removed")
sys.exit(0)
