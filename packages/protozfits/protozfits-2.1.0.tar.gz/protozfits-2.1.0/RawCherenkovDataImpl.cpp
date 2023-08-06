#include "RawCherenkovDataImpl.h"
#include "AnyArrayHelper.h"
  
    ///////////////////////////////////////////////////////////////////////
    //   HIGH RES TIMESTAMP CONSTRUCTOR                                  //
    ///////////////////////////////////////////////////////////////////////
    CTA::HighResTimestamp::HighResTimestamp(uint32 sec, uint32 nanosec)
    {
        s = sec;
        qns = nanosec;
    }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///                                                                         ///
//////                 CAMERA CONFIGURATION METHODS                      //////
///                                                                         ///
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////////////////////
    //   CONSTRUCTOR                                                     //
    ///////////////////////////////////////////////////////////////////////
    CTA::CameraConfiguration::CameraConfiguration()
    {

    }

    ///////////////////////////////////////////////////////////////////////
    //   DESTRUCTOR                                                      //
    ///////////////////////////////////////////////////////////////////////
    CTA::CameraConfiguration::~CameraConfiguration()
    {

    }

    ///////////////////////////////////////////////////////////////////////
    //   GET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    uint16  CTA::CameraConfiguration::getTelId()
    {
        return proto_object.tel_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    uint64  CTA::CameraConfiguration::getLocalRunId()
    {
        return proto_object.local_run_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CONFIG TIME                                                 //
    ///////////////////////////////////////////////////////////////////////
    CTA::HighResTimestamp CTA::CameraConfiguration::getConfigTime()
    {
        return HighResTimestamp(proto_object.config_time_s(), proto_object.config_time_qns());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CAMERA CONFIG ID                                            //
    ///////////////////////////////////////////////////////////////////////
    uint64  CTA::CameraConfiguration::getCameraConfigId()
    {
        return proto_object.camera_config_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET PIXEL ID MAP                                                //
    ///////////////////////////////////////////////////////////////////////
    uint16* CTA::CameraConfiguration::getPixelIdMap()
    {
        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object.mutable_pixel_id_map(), 
                                                      proto_object.num_pixels());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET MODULE ID MAP                                               //
    ///////////////////////////////////////////////////////////////////////
    uint16* CTA::CameraConfiguration::getModuleIdMap()
    {
        assert(proto_object.num_modules() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object.mutable_module_id_map(), 
                                                      proto_object.num_modules());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    uint16  CTA::CameraConfiguration::getNumPixels()
    {
        return proto_object.num_pixels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM MODULES                                                 //
    ///////////////////////////////////////////////////////////////////////
    uint16  CTA::CameraConfiguration::getNumModules()
    {
        return proto_object.num_modules();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    uint8 CTA::CameraConfiguration::getNumChannels()
    {
        return proto_object.num_channels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET DATA MODEL VERSION                                          //
    ///////////////////////////////////////////////////////////////////////
    const string& CTA::CameraConfiguration::getDataModelVersion()
    {
        return proto_object.data_model_version();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CALIBRATION SERVICE ID                                      //
    ///////////////////////////////////////////////////////////////////////
    uint64 CTA::CameraConfiguration::getCalibrationServiceId()
    {
        return proto_object.calibration_service_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CALIBRATION ALGORITHM ID                                    //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::CameraConfiguration::getCalibrationAlgorithmId()
    {
        return proto_object.calibration_algorithm_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM SAMPLES NOMINAL                                         //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::CameraConfiguration::getNumSamplesNominal()
    {
        return proto_object.num_samples_nominal();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM SAMPLES LONG                                            //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::CameraConfiguration::getNumSamplesLong()
    {
        return proto_object.num_samples_long();
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setLocalRunId(uint64 id)
    {
        proto_object.set_local_run_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setTelId(uint16 id)
    {
        proto_object.set_tel_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CONFIG TIME                                                 //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setConfigTime(HighResTimestamp ts)
    {
        proto_object.set_config_time_s(ts.s);
        proto_object.set_config_time_qns(ts.qns);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CAMERA CONFIG ID                                            //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setCameraConfigId(uint64 id)
    {
        proto_object.set_camera_config_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setNumPixels(uint16 num_pixels)
    {
        proto_object.set_num_pixels(num_pixels);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM MODULES                                                 //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setNumModules(uint16 num_modules)
    {
        proto_object.set_num_modules(num_modules);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setNumChannels(uint8 num_channels)
    {
        proto_object.set_num_channels(num_channels);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET DATA MODEL VERSION                                          //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setDataModelVersion(const string& version)
    {
        proto_object.set_data_model_version(version);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CALIBRATION SERVICE ID                                      //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setCalibrationServiceId(uint64 id)
    {
        proto_object.set_calibration_service_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CALIBRATION ALGORITHM ID                                    //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setCalibrationAlgorithmId(uint16 id)
    {
        proto_object.set_calibration_algorithm_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM SAMPLES NOMINAL                                         //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setNumSamplesNominal(uint16 num_samples_nominal)
    {
        proto_object.set_num_samples_nominal(num_samples_nominal);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM SAMPLES LONG                                            //
    ///////////////////////////////////////////////////////////////////////
    void CTA::CameraConfiguration::setNumSamplesLong(uint16 num_samples_long)
    {
        proto_object.set_num_samples_long(num_samples_long);
    }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///                                                                         ///
//////                 CAMERA CONFIGURATION METHODS                      //////
///                                                                         ///
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////////////////////
    //   CONSTRUCTOR                                                     //
    ///////////////////////////////////////////////////////////////////////
    CTA_R1::Event::Event()
    {

    }

    ///////////////////////////////////////////////////////////////////////
    //   DESTRUCTOR                                                      //
    ///////////////////////////////////////////////////////////////////////
    CTA_R1::Event::~Event()
    {

    }

    ///////////////////////////////////////////////////////////////////////
    //   GET EVENT ID                                                    //
    ///////////////////////////////////////////////////////////////////////
    uint64 CTA_R1::Event::getEventId()
    {
        return proto_object.event_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA_R1::Event::getTelId()
    {
        return proto_object.tel_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    uint64 CTA_R1::Event::getLocalRunId()
    {
        return proto_object.local_run_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET EVENT TYPE                                                  //
    ///////////////////////////////////////////////////////////////////////
    uint8 CTA_R1::Event::getEventType()
    {
        return proto_object.event_type();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET EVENT TIME                                                  //
    ///////////////////////////////////////////////////////////////////////
    CTA::HighResTimestamp CTA_R1::Event::getEventTime()
    {
        return CTA::HighResTimestamp(proto_object.event_time_s(), proto_object.event_time_qns());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    uint8 CTA_R1::Event::getNumChannels()
    {
        return proto_object.num_channels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM SAMPLES                                                 //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA_R1::Event::getNumSamples()
    {
        return proto_object.num_samples();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA_R1::Event::getNumPixels()
    {
        return proto_object.num_pixels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET WAVEFORM                                                    //
    ///////////////////////////////////////////////////////////////////////
    uint16* CTA_R1::Event::getWaveform()
    {
        assert(proto_object.num_channels() != 0);
        assert(proto_object.num_samples()  != 0);
        assert(proto_object.num_pixels()   != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object.mutable_waveform(),
                                                      proto_object.num_channels()*proto_object.num_samples()*proto_object.num_pixels());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET PIXEL STATUS                                                //
    ///////////////////////////////////////////////////////////////////////
    uint16* CTA_R1::Event::getPixelStatus()
    {
        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object.mutable_pixel_status(),
                                                      proto_object.num_pixels());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET FIRST CELL ID                                               //
    ///////////////////////////////////////////////////////////////////////
    uint32* CTA_R1::Event::getFirstCellId()
    {
        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint32>(proto_object.mutable_pixel_status(),
                                                      proto_object.num_pixels());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET MODULE HIRES LOCAL CLOCK COUNTER                            //
    ///////////////////////////////////////////////////////////////////////
    uint64* CTA_R1::Event::getModuleHiresLocalClockCounter()
    {
        assert(proto_object.num_modules() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint64>(proto_object.mutable_module_hires_local_clock_counter(),
                                                      proto_object.num_modules());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET PEDESTAL INTENSITY                                          //
    ///////////////////////////////////////////////////////////////////////
    float* CTA_R1::Event::getPedestalIntensity()
    {

        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::reallocAs<float>(proto_object.mutable_pedestal_intensity(),
                                                     proto_object.num_pixels());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CALIBRATION MONITORING ID                                   //
    ///////////////////////////////////////////////////////////////////////
    uint64 CTA_R1::Event::getCalibrationMonitoringId()
    {
        return proto_object.calibration_monitoring_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET EVENT ID                                                    //
    ///////////////////////////////////////////////////////////////////////
    void CTA_R1::Event::setEventId(uint64 id)
    {
        proto_object.set_event_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    void CTA_R1::Event::setTelId(uint16 tel_id)
    {
        proto_object.set_tel_id(tel_id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    void CTA_R1::Event::setLocalRunId(uint64 local_run_id)
    {
        proto_object.set_local_run_id(local_run_id);
    }

    ///////////////////////////////////////////////////////////////////////
    //                           CONSTRUCTOR                             //
    ///////////////////////////////////////////////////////////////////////
    void CTA_R1::Event::setEventType(uint8 type)
    {
        proto_object.set_event_type(type);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET EVENT TIME                                                  //
    ///////////////////////////////////////////////////////////////////////
    void CTA_R1::Event::setEventTime(CTA::HighResTimestamp time)
    {
        proto_object.set_event_time_s(time.s);
        proto_object.set_event_time_qns(time.qns);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    void CTA_R1::Event::setNumChannels(uint8 num_chans)
    {
        proto_object.set_num_channels(num_chans);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM SAMPLES                                                 //
    ///////////////////////////////////////////////////////////////////////
    void CTA_R1::Event::setNumSamples(uint16 num_samples)
    {
        proto_object.set_num_samples(num_samples);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    void CTA_R1::Event::setNumPixels(uint16 num_pixels)
    {
        proto_object.set_num_pixels(num_pixels);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CALIBRATION MONITORING ID                                   //
    ///////////////////////////////////////////////////////////////////////
    void CTA_R1::Event::setCalibrationMonitoringId(uint64 id)
    {
        proto_object.set_calibration_monitoring_id(id);
    }


///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///                                                                         ///
//////               INTERNAL HELPERS SPECIALIZATION                     //////
///                                                                         ///
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

template <>
MessageType getMessageEnum<CTA_R1::Event>()
{
    return R1_EVENT;
}

template<>
MessageType getMessageEnum<CTA::CameraConfiguration>()
{
    return CAMERA_CONFIG;
}
