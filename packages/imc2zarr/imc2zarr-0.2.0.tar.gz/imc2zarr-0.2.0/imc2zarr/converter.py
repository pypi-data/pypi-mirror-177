from pathlib import Path
import json

import xarray as xr

from .imclib.imcraw import ImcRaw


class Imc2Zarr:

    def __init__(self, input_path, output_path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.output_fn = None

    def convert(self):
        imc_scans = []
        auxiliary_imc_scans = []
        input_name = self.input_path.name
        txt_fns = list(self.input_path.glob('*.txt'))
        try:
            # check whether the input_path points to an mcd file or a folder
            if self.input_path.is_file():
                if self.input_path.suffix != '.mcd':
                    raise Exception('Input file does not seem to be a valid mcd file')
                imc_scans.append(ImcRaw(self.input_path, txt_fns=txt_fns))
                input_name = input_name[: -len(self.input_path.suffix)]
            else:
                # check if mcd file exists
                mcd_files = list(self.input_path.glob('*.mcd'))
                if not mcd_files:
                    raise Exception('No mcd file was found in the input folder')
                for mcd_fn in mcd_files:
                    imc_scans.append(ImcRaw(mcd_fn, txt_fns=txt_fns))
            # check if there is a data mcd file
            data_imc_scans = [imc for imc in imc_scans if imc.has_acquisitions]
            # auxiliary scans that only contain image snapshots
            auxiliary_imc_scans = [imc for imc in imc_scans if not imc.has_acquisitions]
            if len(data_imc_scans) > 1:
                raise Exception('More than one mcd data files were found in the input folder')
            elif len(data_imc_scans) < 1:
                raise Exception('Could not find an mcd file with acquisition data')
            # run the conversion
            data_imc_scan = data_imc_scans[0]
            self.output_fn = self.output_path.joinpath(
                '{}_{}'.format(input_name, data_imc_scan.code)
            )
            # save acquisitions into Zarr
            self._convert2zarr(data_imc_scan)
            # save raw metadata and snapshots
            self._save_auxiliary_data(
                data_imc_scan,
                xml_path=self.output_fn,
                snapshots_path=self.output_fn.joinpath('snapshots')
            )
            # save raw metadata and snapshots from auxiliary mcd files
            for aux_scan in auxiliary_imc_scans:
                auxiliary_output_path = 'auxiliary/{}'.format(
                    aux_scan.mcd_fn.name[: -len(aux_scan.mcd_fn.suffix)]
                )
                auxiliary_output_path = self.output_fn.joinpath(auxiliary_output_path)
                self._save_auxiliary_data(
                    aux_scan,
                    xml_path=auxiliary_output_path,
                    snapshots_path=auxiliary_output_path
                )
        finally:
            for imc_scan in imc_scans:
                imc_scan.close()

    def _convert2zarr(self, imc: ImcRaw):
        ds = xr.Dataset()
        # set meta for root
        ds.attrs['meta'] = [json.loads(json.dumps(imc.meta_summary, default=str))]
        ds.attrs['raw_meta'] = imc.rawmeta
        ds.to_zarr(self.output_fn, mode='w')
        # loop over all acquisitions to read and store channel data
        for q in imc.acquisitions:
            data = imc.get_acquisition_data(q)
            nchannels, ny, nx = data.shape
            q_name = 'Q{}'.format(str(q.id).zfill(3))
            ds_q = xr.Dataset()
            arr = xr.DataArray(
                data,
                dims=('channel', 'y', 'x'),
                name='data',
                coords={
                    'channel': range(nchannels),
                    'y': range(ny),
                    'x': range(nx)
                },
            )
            arr.attrs['meta'] = [json.loads(json.dumps(q.meta_summary, default=str))]
            ds_q[q_name] = arr
            ds_q.attrs['meta'] = arr.attrs['meta']
            # append acquisition to existing dataset
            ds_q.to_zarr(self.output_fn, group=q_name, mode='a')

    def _save_auxiliary_data(self, imc: ImcRaw, xml_path, snapshots_path):
        # save raw meta as xml file
        imc.save_meta_xml(xml_path)
        # save snapshots
        imc.save_snapshot_images(snapshots_path)
