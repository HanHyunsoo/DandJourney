# 定义队列类, 还没做并发처리 중

import sys
import datetime

"""
대기열 및 대기열 관리자Job
단일 순간에 작업을 할당하는 프로젝트의 통합 관리를 위한 대기열
작업Job대상 검색 대기열뿐만 아니라 대기열 삽입 및 삭제를 위해

아직 완료되지 않음
"""

class QueueCls:
    def __init__(self, queue_name, queue_size, queue_value, is_isolation):
        """
        queue_name : 대기열 이름
        queue_size : 대기열 크기(비메모리 크기)
        queue_value : 대기열 값
        is_isolation : 대기열이 격리되어 있습니다(대기열 패턴을 지능적으로 삽입하는 데 사용됩니다.)
        """
        self.queue_name = queue_name
        self.queue_size = queue_size
        self.queue_value = queue_value
        self.is_isolation = is_isolation
        self.queue = []

    def get_unused_job_id(self, UpJob):
        """
        큐를 참조하지 않음JobID
        """
        used_ids = [item['JobID'][10:] for item in self.queue]
        _date = datetime.datetime.now().strftime("%m%d%H%M%S")
        if len(used_ids) >= self.queue_size:pass
        else:
            if UpJob:return (True, UpJob)
            for i in range(self.queue_size):
                new_id = "{}{}{}".format(_date, self.queue_name, i)
                if new_id not in used_ids:
                    return (True, new_id)
        return (False, "JobID has already reach limit:{}".format(self.queue_size))

    def insert(self, element, otherKey, UpJob):
        """
        대기열 값 삽입
        """
        job_id = self.get_unused_job_id(UpJob)
        if job_id[0]:
            element["JobID"] = job_id[1] + otherKey
            self.queue.append(element)
        return job_id

    def remove(self, job_id):
        """
        대기열 값 삭제
        """
        removed_elements = []
        for item in self.queue:
            if item.get('JobID') == job_id:
                self.queue.remove(item)
                removed_elements.append(item)
        return removed_elements

    def find(self, any_key, any_value, dim = None):
        "키-값 쌍을 기반으로 대기열 요소 찾기"
        return [item for item in self.queue if item[any_key][:dim] == any_value]

    def extract(self):
        """
        큐 유효성 검사
        """
        if self.queue:
            return (True, self.queue[0])
        else:
            return (False, "Queue is empty.")

    def last(self, PutAll = False, length = False):
        """
        남은 대기열 출력
        """
        if PutAll:
            return [item for item in self.queue]
        if length:
            return len(self.queue)
        else:
            return [item['JobID'] for item in self.queue]
        
    def get_memory(self):
        """
        대기열에 대한 공간 확보
        """
        total_memory = sum(sys.getsizeof(item) for item in self.queue)
        return total_memory


class Job:
    def __init__(self):
        self.queues = {}

    def create_queue(self, queue_name, queue_size, queue_value, is_isolation=False):
        """
        대기열 생성
        """
        if queue_name not in self.queues:
            self.queues[queue_name] = QueueCls(queue_name, queue_size, queue_value, is_isolation)
            print(f"Queue '{queue_name}' created.")
        else:
            print(f"Queue '{queue_name}' already exists.")

    def delete_queue(self, queue_name):
        """
        대기열 삭제
        """
        if queue_name in self.queues:
            del self.queues[queue_name]
            print(f"Queue '{queue_name}' deleted.")
        else:
            print(f"Queue '{queue_name}' does not exist.")

    def find_queue(self, queue_name):
        """
        대기열 이름으로 대기열 찾기
        """
        if queue_name in self.queues:
            return (True, self.queues[queue_name])
        else:
            return (False, f"Queue '{queue_name}' does not exist.")

    def queueList(self):
        """
        출력 대기열 목록
        """
        return [_queue for _queue in self.queues.keys()]
    
    def queueAllItem(self, PutAll = False, length = False):
        """
        모든 큐의 모든 요소 출력
        """
        return [self.queues[_queue].last(PutAll, length) for _queue in self.queues.keys()]
    
    def insert_queue(self, queue_name, element, UpJob = "", otherKey = ""):
        """
        지정된 큐에 요소를 삽입합니다
        """
        if queue_name in self.queues:
            queue = self.queues[queue_name]
            inserted_job_id = queue.insert(element, otherKey, UpJob)
            return inserted_job_id, queue_name
        else:
            return (False, "Queue does not exist")

    def insert_queue_S(self, element, authority, NoneQueue, UpJob = "", otherKey = ""):
        """
        스마트 인서트 큐 모드
        이 방법을 사용하여 데이터를 삽입하고 조건에 따라 삽입 조건을 충족하는 대기열을 자동으로 선택하는 스마트 삽입을 엽니다.
        현재 상태:삽입할 대기열 길이가 가장 짧은 요소를 선택합니다.
        """
        if authority:
            queue_to_insert = min((q for q in self.queues.values() if not q.is_isolation), key=lambda q: q.last(length = True))
        else:
            queue_to_insert = next((q for q in self.queues.values() if q.queue_name == NoneQueue), None)

        if queue_to_insert:
            inserted_job_id = queue_to_insert.insert(element, otherKey, UpJob)
            return inserted_job_id, queue_to_insert.queue_name
        else:
            return (False, "Can't find Queue in JobList")

    def delete_queue_value(self, queue_id, job_id):
        """
        지정된 대기열에서 삭제JobID포인팅 요소
        """
        if queue_id in self.queues:
            queue = self.queues[queue_id]
            removed_elements = queue.remove(job_id)
            return removed_elements
        else:
            print(f"Queue '{queue_id}' does not exist.")
            return []
        
    def get_memory(self):
        """
        쿼리 큐 관리자 현재 메모리
        큐에 객체가 나타나면 이 알고리즘이 유효하지 않습니다.
        """
        total_memory = sum(queue.get_memory() for queue in self.queues.values())
        return total_memory
