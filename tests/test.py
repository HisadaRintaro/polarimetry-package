from polarimetry_package.models import InstrumentModel, RectangleArea, CircleArea, Wave
from polarimetry_package.pipeline import run_pipeline

directry= "FOC_POL_C1F/"
area = RectangleArea(x0=300, x1=400, y0=100, y1=200) 
circle = CircleArea(radius=50, cx=350, cy=150)
background_area = circle
image_area = RectangleArea(x0=13, x1=43, y0=15, y1=51)
wave = Wave(1000,10000,5000)
bin_size = 10


instrument: InstrumentModel = InstrumentModel(file_directry=directry, suffix= "", extension= "")

result = run_pipeline(instrument, background_area, bin_size, wave, method="median")

#image plottings
from polarimetry_package import plotting
pa_ax = plotting.plot_position_angle(
        result.raws.data["POL0"],
        result.position_angle.theta,
        bin_size,
        stretch="log"
        )
pa_ax = background_area.plot_region(ax=pa_ax)


#transmittance curves
from polarimetry_package.models import MuellerMatrixFactory
mueller_matrix_factory = MuellerMatrixFactory.load(result.flux.hdr_profile, wave)
trans_ax = mueller_matrix_factory.plot_transmittance_curve(wave)

#stokes panel
from polarimetry_package.plotting import show_stokes_panel
show_stokes_panel(result.stokes.I, result.stokes.Q, result.stokes.U)
