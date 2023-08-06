from __future__ import absolute_import


def do_cache_transformation(cache, attributes={}, site_id=None):
        # extract cache filters from ImageCache object
        img_obj = cache.content_type.model_class()._base_manager.get(pk=cache.object_id)
        img_field = cache.field_name
        filters = cache.filters.split('__') if cache.filters else []
        imgfile = getattr(img_obj, img_field)
        size = cache.width, cache.height

        # get the backends and related information
        backend_dict = backends_pool.get_imagecache_backends_dict()
        default_backend = backend_dict[cache.backend]
        img_location = imgfile.path
        db_file = False

        # site id must be set in order to generate the proper s3 path
        if getattr(settings, 'CELERY_GEN_CACHE', False) and site_id:
            settings.SITE_ID = site_id

        if img_location == "DBHASH":
            img_location = imgfile.name
            db_file = True
        try:
            transform = TransformImage(imgfile.file, size[0], size[1])
        except IOError:
            raise ImageCacheError('The image file for image "%s" is missing.' % img_obj)

        for filter in filters:
            transform.apply_filter(filter)

        if transform.format.upper() in ("JPG", "JPEG"):
            format = transform.format
        else:
            format = "png"

        alt = None
        if "alt" in attributes:
            alt = attributes['alt']

        if db_file:
            parts = img_location.split(',')
            original_filename = parts[1][5:]
        else:
            original_filename = imgfile.name

        file_path = default_backend.store(cache, transform, original_filename, alt, format)

        cache.image = file_path
        cache.backend = default_backend.backend_name
        cache.processed = True
        cache.save()
        return True

