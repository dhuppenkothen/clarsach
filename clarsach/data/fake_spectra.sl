#! /usr/bin/env isis

variable EXPOSURE = 100.e3;  % A 100 ks exposure time
variable NORM = 1.0, PHOINDEX = 2.0;

variable acis_arf, acis_rmf, acis=1;

acis_arf = load_arf("arfs/aciss_hetg0_cy19.arf");
acis_rmf = load_rmf("rmfs/aciss_hetg0_cy19.rmf");

assign_arf(acis_arf, acis);
assign_rmf(acis_rmf, acis);

% Set the exposure time
set_arf_exposure(acis, EXPOSURE);
set_data_exposure(acis, EXPOSURE);

% Start simulating the thing
fit_fun("powerlaw(1)");
set_par("powerlaw(1).norm", NORM);
set_par("powerlaw(1).PhoIndex", PHOINDEX);

% Freeze parameters in place (no reason, really, just in case)
freeze("powerlaw(1).*");

% Now simulate the spectrum
fakeit;
fits_write_pha_file("fake_acis.pha", acis);

%% --- Now do the HETG data --- %%

variable heg_p1=2, heg_m1=3, heg_p1_arf, heg_m1_arf, heg_p1_rmf, heg_m1_rmf;
variable meg_p1=4, meg_m1=5, meg_p1_arf, meg_m1_arf, meg_p1_rmf, meg_m1_rmf;

heg_p1_arf = load_arf("arfs/aciss_heg1_cy19.garf");
heg_m1_arf = load_arf("arfs/aciss_heg-1_cy19.garf");

meg_p1_arf = load_arf("arfs/aciss_meg1_cy19.garf");
meg_m1_arf = load_arf("arfs/aciss_meg-1_cy19.garf");

heg_p1_rmf = load_rmf("rmfs/aciss_heg1_cy19.grmf");
heg_m1_rmf = load_rmf("rmfs/aciss_heg-1_cy19.grmf");

meg_p1_rmf = load_rmf("rmfs/aciss_meg1_cy19.grmf");
meg_m1_rmf = load_rmf("rmfs/aciss_meg-1_cy19.grmf");

assign_arf(heg_p1_arf, heg_p1);
assign_arf(heg_m1_arf, heg_m1);
assign_arf(meg_p1_arf, meg_p1);
assign_arf(meg_m1_arf, meg_m1);

assign_rmf(heg_p1_rmf, heg_p1);
assign_rmf(heg_m1_rmf, heg_m1);
assign_rmf(meg_p1_rmf, meg_p1);
assign_rmf(meg_m1_rmf, meg_m1);

set_arf_exposure([heg_p1, heg_m1, meg_p1, meg_m1], EXPOSURE);

variable i;
foreach i ([heg_p1, heg_m1, meg_p1, meg_m1]) set_data_exposure(i, EXPOSURE);

fakeit;

fits_write_pha_file("fake_heg_p1.pha", heg_p1);
fits_write_pha_file("fake_heg_m1.pha", heg_m1);
fits_write_pha_file("fake_meg_p1.pha", meg_p1);
fits_write_pha_file("fake_meg_m1.pha", meg_m1);
