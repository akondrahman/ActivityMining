#https://api.github.com/repos/hadley/dplyr/issues
#reff: https://blog.exploratory.io/analyzing-issue-data-with-github-rest-api-63945017dedc

curl -H "Authorization: token <TOKEN_GOES_HERE>" -ni "https://api.github.com/repos/JuliaLang/julia/issues" -H 'Accept: json' > JuliaIssues.json