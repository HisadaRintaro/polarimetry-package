from ..models.instrument import InstrumentModel
from ..models.image_set import ImageSet
from ..models.flux_image import FluxImage
from ..models.stokes_set import StokesParameter, PolarizationDegree, PositionAngle
from ..models.transmittance import Wave
from ..models.area import Area
from ..models.result import PolarimetryResult

def run_pipeline(
    instrument: InstrumentModel,
    area: Area,
    bin_size: int,
    wave: Wave,
    method= "median",
    p_mask = 3,
):
    images = (
        ImageSet.load(instrument)
        .sum()
        .align()
        .backfground_subtract(area, method=method)
        .binning(bin_size)
    )
    flux = FluxImage.load(images)
    stokes = StokesParameter.load(flux, wave)
    polarization_degree = PolarizationDegree.load(stokes)
    if p_mask:
        mask = polarization_degree.make_mask(ratio=p_mask)
        position_angle = PositionAngle.load(stokes, mask=mask)
    else:
        position_angle = PositionAngle.load(stokes)

    return PolarimetryResult(
            raws= ImageSet.load(instrument).sum(),
            images= images,
            flux= flux,
            stokes= stokes,
            polarization_degree= polarization_degree,
            position_angle= position_angle,
            )
