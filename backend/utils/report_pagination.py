from rest_framework.response import Response


def get_page_and_size(request, default_size=20, max_size=100):
    """
    Extract page and page_size safely from query params.
    Supports:
      - ?page=2&page_size=20
      - ?params[page]=2&params[page_size]=20
    """
    page_param = request.query_params.get('page') or request.query_params.get('params[page]')
    size_param = request.query_params.get('page_size') or request.query_params.get('params[page_size]')

    try:
        page = max(1, int(page_param)) if page_param else 1
    except (ValueError, TypeError):
        page = 1

    try:
        page_size = min(max_size, max(1, int(size_param))) if size_param else default_size
    except (ValueError, TypeError):
        page_size = default_size

    return page, page_size


def paginate_records(records, request, default_size=20, max_size=100):
    """
    Paginates a Django QuerySet or Python list.
    Returns:
        paginated_slice: sliced QuerySet or list
        pagination_meta: dictionary matching CustomDataTable expectations
    """
    page, page_size = get_page_and_size(request, default_size, max_size)

    if isinstance(records, (list, tuple)):
        total_count = len(records)
    elif hasattr(records, 'count') and callable(records.count):
        total_count = records.count()
    else:
        total_count = len(records)

    num_pages = max(1, (total_count + page_size - 1) // page_size) if total_count > 0 else 1
    if page > num_pages:
        page = 1

    start = (page - 1) * page_size
    end = start + page_size

    paginated_items = records[start:end]

    pagination_meta = {
        'count': total_count,
        'total': total_count,
        'num_pages': num_pages,
        'current_page': page,
        'page_size': page_size,
    }

    return paginated_items, pagination_meta


def paginated_report_response(results, pagination_meta, extra=None):
    """
    Constructs a standard paginated DRF Response.
    """
    data = {
        'results': results,
        'count': pagination_meta.get('count', len(results)),
        'pagination': pagination_meta,
    }
    if extra and isinstance(extra, dict):
        data.update(extra)
    return Response(data)
