import requests
from tqdm_pathos import map


def __send_message(message):
    # 생성한 웹훅 주소
    hook = 'https://hooks.slack.com/services/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'
    title = '전처리 완료, 결과를 확인해주세요.'
    content = message

    # 메시지 전송
    requests.post(
        hook,
        headers={'content-type': 'application/json'},
        json={
            'text': title,
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f"{content}건의 결과가 처리되었습니다."
                    }
                }
            ]
        }
    )


def sts(method, *args, cpu):
    result_arr = map(method, *args, n_cpus=cpu)

    result_arr = [i for i in result_arr if i is not None]

    __send_message(len(result_arr))

    return result_arr
