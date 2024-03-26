#***django starter***

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)
 
### Third party libraries
 

[Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

[drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) 

#### Separation of Development and Production Environments
###linux and mac
####development
``` export DJANGO_SETTINGS_MODULE=core.settings.dev```
####production
`export DJANGO_SETTINGS_MODULE=core.settings.prod`

###windows
####develop
`set DJANGO_SETTINGS_MODULE=core.settings.dev`
####production
`set DJANGO_SETTINGS_MODULE=core.settings.prod`

####docker project 

``` docker-compose up -d```

####makemigrations

```docker-compose exec backend sh -c "python manage.py makemigrations --settings core.settings.dev"```

####migrate
```docker-compose exec backend sh -c "python manage.py migrate --settings core.settings.dev"```

####collectstatic
```docker-compose exec backend sh -c "python manage.py collectstatic --settings core.settings.dev"```

