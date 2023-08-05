from __future__ import annotations

import _io
import multiprocessing
from dataclasses import dataclass
from queue import Empty

s_line_template = 'S\t{low_scan}\t{high_scan}\t{mz}\n'
i_line_template = 'I\t{keyword}\t{value}\n'
z_line_template = 'Z\t{charge}\t{mass}\n'
peak_line_template = '{mz} {intensity}\n'
peak_line_charged_template = '{mz} {intensity} {charge}\n'


@dataclass(slots=True)
class Ms2Spectra:
    low_scan: int
    high_scan: int
    mz: float
    mass: float
    charge: int
    info: dict
    mz_spectra: list[float]
    intensity_spectra: list[float]
    charge_spectra: list[float]


def _serialize_ms2_spectra(ms2_spectra: Ms2Spectra) -> str:
    P = 4
    s_line = s_line_template.format(low_scan=ms2_spectra.low_scan, high_scan=ms2_spectra.high_scan, mz=round(ms2_spectra.mz, P))
    i_lines = [i_line_template.format(keyword=k, value=v) for k, v in ms2_spectra.info.items()]
    z_line = z_line_template.format(charge=ms2_spectra.charge, mass=round(ms2_spectra.mass, P))

    if ms2_spectra.charge_spectra:
        peak_lines = [peak_line_charged_template.format(mz=round(m, P), intensity=round(i, 1), charge=c) for m, i, c in
                     zip(ms2_spectra.mz_spectra, ms2_spectra.intensity_spectra, ms2_spectra.charge_spectra)]
    else:
        peak_lines = [peak_line_template.format(mz=round(m, P), intensity=round(i, 1)) for m, i in
                     zip(ms2_spectra.mz_spectra, ms2_spectra.intensity_spectra)]

    return ''.join([s_line] + i_lines + [z_line] + peak_lines)


def _deserialize_ms2_spectra(spectra_str: str | list[str], include_spectra=True) -> Ms2Spectra:
    if type(spectra_str) is str:
        lines = spectra_str.split('\n')
    elif type(spectra_str) is list:
        lines = spectra_str
    else:
        raise ValueError(f'Unsupported spectra_str type: {type(spectra_str)}!')

    low_scan, high_scan, mz, mass, charge = None, None, None, None, None
    info, mz_spectra, intensity_spectra, charge_spectra = {}, [], [], []

    for line in lines:
        if line[0] == 'S':
            line_elems = line.rstrip().split('\t')
            low_scan = int(line_elems[1])
            high_scan = int(line_elems[2])
            mz = float(line_elems[3])
        elif line[0] == 'Z':
            line_elems = line.rstrip().split('\t')
            charge = int(line_elems[1])
            mass = float(line_elems[2])
        elif line[0] == 'I':
            line_elems = line.rstrip().split('\t')
            info[line_elems[1]] = '\t'.join(line_elems[2:])
        elif line[0].isnumeric() and include_spectra:
            line_elems = line.rstrip().split(' ')
            mz_spectra.append(float(line_elems[0]))
            intensity_spectra.append(float(line_elems[1]))
            if len(line_elems) == 3:
                charge_spectra.append(float(line_elems[2]))

    return Ms2Spectra(low_scan=low_scan,
                      high_scan=high_scan,
                      mz=mz,
                      mass=mass,
                      charge=charge,
                      info=info,
                      mz_spectra=mz_spectra,
                      intensity_spectra=intensity_spectra,
                      charge_spectra=charge_spectra)


def ms2_spectra_consumer(queue, return_dict):
    print('Consumer: Running', flush=True)
    # consume work
    while True:
        try:
            tmp_spectra_lines = queue.get(timeout=1)
        except Empty:
            break
        ms2_spectra = _deserialize_ms2_spectra(tmp_spectra_lines)
        return_dict[ms2_spectra.low_scan] = ms2_spectra

    print('Consumer: Stopping')


def from_ms2(ms2_input: str | _io.TextIOWrapper, include_spectra=True, processes=1) -> (list[str], list[Ms2Spectra]):
    if type(ms2_input) is str:
        lines = ms2_input.split('\n')

    elif type(ms2_input) is _io.TextIOWrapper:
        lines = ms2_input

    else:
        raise ValueError(f'Unsupported input type: {type(ms2_input)}!')

    header_lines = []
    spectra = []
    tmp_spectra_lines = []

    multi_process = processes > 1

    if multi_process:
        queue = multiprocessing.Queue()
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

    for line in lines:

        if line.startswith('H'):
            header_lines.append(line)
            continue

        elif line.startswith('S'):
            if tmp_spectra_lines:
                if multi_process:
                    queue.put(tmp_spectra_lines)
                else:
                    spectra.append(_deserialize_ms2_spectra(tmp_spectra_lines, include_spectra))
                tmp_spectra_lines = []

        if line:
            tmp_spectra_lines.append(line)

    if multi_process:
        queue.put(tmp_spectra_lines)
    else:
        spectra.append(_deserialize_ms2_spectra(tmp_spectra_lines, include_spectra))

    if multi_process:
        jobs = []
        for i in range(processes):
            p = multiprocessing.Process(target=ms2_spectra_consumer, args=(queue, return_dict))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        spectra = list(return_dict.values())

    return header_lines, spectra


def to_ms2(h_lines: list[str], ms2_spectras: list[Ms2Spectra]) -> str:
    lines = []
    for h_line in h_lines:  # Write header lines
        if h_line.endswith('\n'):
            lines.append(h_line)
        else:
            lines.append(h_line + '\n')

    for ms2_spectra in ms2_spectras:
        lines.append(_serialize_ms2_spectra(ms2_spectra))

    return ''.join(lines)
