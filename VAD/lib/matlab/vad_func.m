function [ data_len, winlen, winstep ] = vad_func( audio_dir )
    
    system('rm -rf result');
    system('rm -rf sample_data');
    
    disp('MRCG extraction ...')
    [data_len, winlen, winstep] = mrcg_extract( audio_dir );
     
end

