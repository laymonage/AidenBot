"""
Indonesian 2019 presidential election helper module.

(c) 2019 - laymonage
"""

import datetime
import json
import requests


def get_election_data():
    """Return the data from KPU."""
    version = 'https://pemilu2019.kpu.go.id/static/json/version.json'
    ppwp = 'https://pemilu2019.kpu.go.id/static/json/hhcw/ppwp.json'
    version, ppwp = requests.get(version), requests.get(ppwp)
    version, ppwp = json.loads(version.content), json.loads(ppwp.content)

    version = _process_version(version['version'])
    chart = _process_chart(ppwp['chart'])
    progress = _process_progress(ppwp['progress'])
    return '{version}\n\n{chart}\n\n{progress}'.format(
        version=version, chart=chart, progress=progress
    )


def _process_version(version):
    timestamp = datetime.datetime.strptime(version, '%Y-%m-%d %H:%M:%S')
    timestamp += datetime.timedelta(hours=7)
    version = timestamp.strftime('%A, %d %B %Y %H:%M:%S')
    return version


def _process_chart(ppwp_chart):
    suara_jokowi = ppwp_chart['21']
    suara_prabowo = ppwp_chart['22']
    jumlah = suara_jokowi + suara_prabowo
    persentase_jokowi = suara_jokowi / jumlah * 100
    persentase_prabowo = suara_prabowo / jumlah * 100

    jokowi = "(01) Joko Widodo - Ma'ruf Amin"
    prabowo = "(02) Prabowo Subianto - Sandiaga Salahudin Uno"

    result = (
        '{jokowi}\n'
        '{s_jokowi} ({p_jokowi:.2f})%\n'
        '\n'
        '{prabowo}\n'
        '{s_prabowo} ({p_prabowo:.2f})%'
    )
    return result.format(
        jokowi=jokowi, s_jokowi=suara_jokowi, p_jokowi=persentase_jokowi,
        prabowo=prabowo, s_prabowo=suara_prabowo, p_prabowo=persentase_prabowo
    )


def _process_progress(ppwp_progress):
    proses = ppwp_progress['proses']
    total = ppwp_progress['total']
    progress_p = proses / total * 100

    result = (
        'Progress: {proses} out of {total} TPS ({progress_p:.5f}%)'
    )
    return result.format(proses=proses, total=total, progress_p=progress_p)
