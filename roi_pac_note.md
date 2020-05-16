For each ROI_PAC-processed scene, the following files should be located in a directory with the format “f$frame_o$orbit/int_$date1_$date2":
		
    $date1_$date2_baseline.rsc
		
    $date1-$date2.amp.rsc
		
    $date1-$date2_2rlks.amp.rsc
		
    $date1-$date2-sim_SIM_2rlks.int.rsc
		
    geo_$date1-$date2_2rlks.amp
		
    geo_$date1-$date2_2rlks.cor	
		
    geo_$date1-$date2_2rlks.cor.rsc
		
***Note: ROI_PAC’s process_2pass.pl should be run with 2 range looks and 10 azimuth looks in both coherence estimation and multi-looking  (equivalent to a 30m-by-30m area for JAXA’s ALOS), with the following lines added to the process file:***
		
    Rlooks_int = 2
		
    Rlooks_sim = 2
		
    Rlooks_sml = 2
		
    pixel_ratio = 5

***A 5-point triangle window is hardcoded in ROI_PAC, which is equivalent to a 2-point rectangle window. For further details on running ROI_PAC see the ROI_PAC manual.***
