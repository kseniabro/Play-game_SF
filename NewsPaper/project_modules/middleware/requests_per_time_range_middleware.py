from collections import defaultdict
import time

from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _


class RequestsPerTimeRangeMiddleWare:
    """
    Ограничение количества запросов от определенного пользователя за определенный промежуток времени.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.times_of_requests = defaultdict(list)

    def __call__(self, request):
        TIME_RANGE = 5
        ALLOWED_NUMBER_OF_REQUESTS = 10

        ip = request.META.get('REMOTE_ADDR')
        current_time = time.time()
        self.times_of_requests[ip].append(current_time)

        number_of_requests = 0
        for i, time_request in enumerate(self.times_of_requests[ip][::-1]):
            if current_time - time_request <= TIME_RANGE:
                number_of_requests += 1
                if number_of_requests > ALLOWED_NUMBER_OF_REQUESTS:
                    print(_("{ip}, Превышено разрешенное количество запросов").format(ip=ip))
                    raise PermissionDenied(_("{ip}, Превышено разрешенное количество запросов").format(ip=ip))
            else:
                self.times_of_requests[ip] = self.times_of_requests[ip][-i:]
                break

        ips_to_remove = []
        for request_ip, request_times in self.times_of_requests.items():
            if current_time - request_times[-1] > TIME_RANGE:
                ips_to_remove.append(request_ip)

        for ip_to_remove in ips_to_remove:
            self.times_of_requests.pop(ip_to_remove)

        response = self.get_response(request)

        return response
