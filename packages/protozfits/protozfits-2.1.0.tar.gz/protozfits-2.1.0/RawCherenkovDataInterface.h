/**
    @file RawCherenkovDataInterface.h

    @brief Abstraction of the interface between ACADA and Cherenkov camera raw data
*/

// use explicit types defined by protocol buffers
// We could define them explicitely instead here, but last time I  tried the (old) gcc 
// compiler had trouble merging the same type being redefined in different headers
#include <google/protobuf/stubs/common.h>

/**
    @namespace CTA
    @brief define all the structures that are to be used mostly everywhere.
*/
namespace CTA
{
    /**
        @struct HighResTimestamp 
        @brief Handling and storage of precise, CTA-style timestamps
    */
    struct HighResTimestamp
    {
        /// Default constructor. Cannot construct unitialized values. Should we ? 
        HighResTimestamp(uint32 sec, uint32 quarternanosec);

        uint32 s;   ///< Seconds in TAI reference. Not yet final: may become UTC after all
        uint32 qns; ///< Quarter nano-seconds elapsed since last second
    };

    /**
        @struct AbstractCameraConfiguration
        @brief  Abstract definition of the camera configuration R1 data model
        Currently in CTA namespace as the same configuration is to be reused for DL0 (AFAIK)
    */
    class AbstractCameraConfiguration
    {
        public:
            /**
                @brief Default constructor. Creates an empty camera configuration
            */
            AbstractCameraConfiguration() {};

            /**
                @brief Default destructor. Releases all allocated memory
            */
            virtual ~AbstractCameraConfiguration() {};

            /**
                @brief Retrieve the telescope ID, called tel_id in data model
            */
            virtual uint16 getTelId() = 0;

            /**
                @brief Retrieve the local run id, called local_run_id in data model
            */
            virtual uint64 getLocalRunId() = 0;

            /**
                @brief Retrieve the configuration time, called config_time in data model
            */
            virtual HighResTimestamp getConfigTime() = 0;

            /**
                @brief Retrieve the camera configuration id, called camera_config_id in data model
            */
            virtual uint64 getCameraConfigId() = 0;

            /**
                @brief Retrieve the pixel id map, called pixel_id_map in data model. 
                Memory allocation performed on-the-fly, according to previously set field
                num_pixels. Memory is reallocated only if the number of pixels changes, and 
                upon querying this method again.
            */
            virtual uint16* getPixelIdMap() = 0;

            /**
                @brief Retrieve the module id map, called module_id_map in data model.
                Memory allocation performed on-the-fly, according to previously set field
                num_modules. Memory is reallocated only if the number of pixels changes, and 
                upon querying this method again.
            */
            virtual uint16* getModuleIdMap() = 0;

            /**
                @brief Retrieve the number of pixels, called num_pixels in data model.
            */
            virtual uint16 getNumPixels() = 0;

            /**
                @brief Retrieve the number of modules, called num_modules in data model
            */
            virtual uint16 getNumModules() = 0;

            /**
                @brief Retrieve the number of channels, called num_channels in data model
            */
            virtual uint8 getNumChannels() = 0;

            /**
                @brief Retrieve the data model version string, called data_model_version in data model
            */
            virtual const std::string& getDataModelVersion() = 0;

            /**
                @brief Retrieve the calibration service id, called calibration_service_id in data model
            */
            virtual uint64 getCalibrationServiceId() = 0;

            /**
                @brief Retrieve the calibration algorithm id, called calibration_algorithm_id in data model
            */
            virtual uint16 getCalibrationAlgorithmId() = 0;

            /**
                @brief Retrieve the nominal number of samples, called num_samples_nominal in data model
            */
            virtual uint16 getNumSamplesNominal() = 0;

            /**
                @brief Retrieve the long number of samples, called num_samples_long in data model
            */
            virtual uint16 getNumSamplesLong() = 0;

            /**
                @brief Set the local run id, called local_run_id in data model
            */
            virtual void setLocalRunId(uint64 id) = 0;

            /**
                @brief Set the telescope id, called tel_id in data model
            */
            virtual void setTelId(uint16 id) = 0;

            /**
                @brief Set the configuration time, called config_time in data model
            */
            virtual void setConfigTime(HighResTimestamp ts) = 0;

            /**
                @brief Set the camera configuration id, called camera_config_id in data model
            */
            virtual void setCameraConfigId(uint64 id) = 0;

            /**
                @brief Set the number of pixels, called num_pixels in data model
            */
            virtual void setNumPixels(uint16 num_pixels) = 0;

            /**
                @brief Set the number of modules, called num_modules in data model
            */
            virtual void setNumModules(uint16 num_modules) = 0;

            /**
                @brief Set the number of channels, called num_channels in data model
            */
            virtual void setNumChannels(uint8 num_channels) = 0;

            /**
                @brief Set the data model version, called data_model_version in data model
            */
            virtual void setDataModelVersion(const std::string& version) = 0;

            /**
                @brief Set the calibration service id, called calibration_service_id in data model
            */
            virtual void setCalibrationServiceId(uint64 id) = 0;

            /**
                @brief Set the calibration algorithm id, called calibration_algorithm_id in data model
            */
            virtual void setCalibrationAlgorithmId(uint16 id) = 0;

            /**
                @brief Set the nominal number of samples, called num_samples_nominal in data model
            */
            virtual void setNumSamplesNominal(uint16 num_samples_nominal) = 0;

            /**
                @brief Set the long number of samples, called num_samples_nominal in data model
            */
            virtual void setNumSamplesLong(uint16 num_samples_long) = 0;
    };
}; //namespace CTA


/**
    @namespace CTA_R1
    @brief Contains everything specific to R1 data model
    Could be renamed to just R1 if this interface is agreed upon
*/
namespace CTA_R1
{
    /**
        @class AbstractEvent
        @brief Abstract definition of the R1 Event data model
    */
    class AbstractEvent
    {
        public:
            /**
                @brief Default constructor. Does nothing.
            */
            AbstractEvent() {};

            /**
                @brief Default destructor. Does nothing
            */
            virtual ~AbstractEvent() {};

            /**
                @brief Retrieve the event id. Called event_id in the data model.
            */
            virtual uint64 getEventId() = 0;

            /**
                @brief Retrieve the telescope id. Called tel_id in the data model.
            */
            virtual uint16 getTelId() = 0;

            /**
                @brief Retrieve the local run id. Called local_run_id in the data model.
            */
            virtual uint64 getLocalRunId() = 0;

            /**
                @brief Retrieve the event type. Called event_type in the data model
            */
            virtual uint8 getEventType() = 0;

            /**
                @brief Retrieve the event time. Called event_time in the data model
            */
            virtual CTA::HighResTimestamp getEventTime() = 0;

            /**
                @brief Retrieve the number of channels. Called num_channels in the data model.
            */
            virtual uint8 getNumChannels() = 0;

            /**
                @brief Retrieve the number of samples. Called num_samples in the data model.
            */
            virtual uint16 getNumSamples() = 0;

            /**
                @brief Retrieve the number of pixels. Called num_pixels in the data model.
            */
            virtual uint16 getNumPixels() = 0;

            /**
                @brief Retrieve the waveforms. Called waveform in the data model.
                Memory allocation performed on-the-fly, according to previously set fields
                num_channels, num_pixels and num_samples. Memory is reallocated only if the 
                number of pixels, channels or samples changes, and upon querying this method again.
            */
            virtual uint16* getWaveform() = 0;

            /**
                @brief Retrieve the pixels status. Called pixel_status in the data model.
                Memory allocation performed on-the-fly, according to previously set field
                num_pixels. Memory is reallocated only if the number of pixels changes, 
                and upon querying this method again.
            */
            virtual uint16* getPixelStatus() = 0;

            /**
                @brief Retrieve the first cell id. Called first_cell_id in the data model.
                Memory allocation performed on-the-fly, according to previously set field
                num_modules. Memory is reallocated only if the number of modules changes, 
                and upon querying this method again.
            */
            virtual uint32* getFirstCellId() = 0;

            /**
                @brief Retrieve the module high resolution clock counters. Called module_hires_local_clock_counter in the data model.
                Memory allocation performed on-the-fly, according to previously set field
                num_modules. Memory is reallocated only if the number of modules changes, 
                and upon querying this method again.
            */
            virtual uint64* getModuleHiresLocalClockCounter() = 0;

            /**
                @brief  Retrieve the pedestal intensity. Called pedestal_intensity in the data model.
                Memory allocation performed on-the-fly, according to previously set field
                num_pixels. Memory is reallocated only if the number of pixels changes, 
                and upon querying this method again.
            */
            virtual float* getPedestalIntensity() = 0;

            /**
                @brief Retrieve the calibration monitoring id. Called calibration_monitoring_id in the data model.
            */
            virtual uint64 getCalibrationMonitoringId() = 0;

            /**
                @brief Set the event id. Called event_id in the data model.
            */
            virtual void setEventId(uint64 id) = 0;

            /**
                @brief Set the telescope id. Called tel_id in the data model.
            */
            virtual void setTelId(uint16 tel_id) = 0;

            /**
                @brief Set the local run id. Called local_run_id in the data model.
            */
            virtual void setLocalRunId(uint64 local_run_id) = 0;

            /**
                @brief Set the event type. Called event_type in the data model.
            */
            virtual void setEventType(uint8 type) = 0;

            /**
                @brief Set the event time. Called event_time in the data model.
            */
            virtual void setEventTime(CTA::HighResTimestamp time) = 0;

            /**
                @brief Set the number of channels. Called num_channels in the data model.
            */
            virtual void setNumChannels(uint8 num_chans) = 0;

            /**
                @brief Set the number of samples. Called num_samples in the data model.
            */
            virtual void setNumSamples(uint16 num_samples) = 0;

            /**
                @brief Set the number of pixels. Called num_pixels in the data model.
            */
            virtual void setNumPixels(uint16 num_pixels) = 0;

            /**
                @brief Set the calibration moniroting id. Called calibration_monitoring_id in the data model.
            */
            virtual void setCalibrationMonitoringId(uint64 id) = 0;
    };
}; //namespace R1

/**
    @class AbstractCherenkovDataStream
    @brief Abstract definition of a generic Cherenkov events streamer
    @tparam CONFIG_ the actual object used to handle Cherenkov camera configuration
    @tparam EVT_ the actual object used to handle Cherenkov camera events
*/
template <class CONFIG_, class EVT_>
class AbstractCherenkovDataStream  
{
    public:
        /**
            @brief Default constructor. Defines a name for this streamer and a mode of operations.
            @param name the name to give to this streamer. Used by ZMQ implementation to visually draw the data flow.
            @param mode the operation mode. Should be either 'r' for reading or 'w' for writing.
        */
        AbstractCherenkovDataStream(const std::string& name, const char mode) {};

        /**
            @brief Default destructor. Frees all objects used and closes any endpoint
        */
        virtual ~AbstractCherenkovDataStream() {};

        /**
            @brief Define where the stream should go. Very implementation specific.
            In the case of the ZMQ implementation, the endpoint string can either be
            a ZMQ configuration string, or a filename. <br>
            In case of a ZMQ configuration, a server would be configured e.g. with:<br>
            tcp://*:1234 <br> to listen on all available interfaces at port 1234. A consumer
            could be configured as <br> tcp://localhost:1234 <br>to connect to localhost at port 1234.
            In case of filenames, the file should not already exist as existing files
            cannot be overridden. <br>
            If a wrong configuration string is given, a runtime_error is thrown. e.g. if 
            the port to use is already taken, or if the target file cannot be written/read.
            Only runtime_errors are thrown, with explenatory message enclosed.
        */
        virtual void SetEndpoint(const std::string& endpoint_config) = 0;

        /**
            @brief Initializes streaming by sending a Cherenkov camera configuration 
            @return the number of bytes written. 0 means that there is not yet a connected peer
        */
        virtual int BeginOutputStream(const CONFIG_& config) = 0;

        /**
            @brief Initializes streaming by reading a Chrenkov camera configuration
            @return the number of bytes read. 0 means that there is not yet a connected peer. -1 means that the stream was terminated
        */
        virtual int BeginInputStream(CONFIG_& config) = 0;

        /**
            @brief Write a Cherenkov event.
            @return the number of bytes written. 0 means that the event couldn't be written e.g. because
            output queues are full, but that otherwise all is well. 
        */
        virtual int WriteEvent(const EVT_& event) = 0;

        /**
            @brief Read a Cherenkov event.
            @return the number of bytes read. 0 means that the event couldn't be read, e.g. because of empty input queues. -1 means that the stream was terminated.
        */
        virtual int ReadEvent(EVT_& event) = 0;

        /**
            @brief End the stream of events.
            In case of a ZMQ streamer, the end-of-stream message is sent out. In all cases this 
            frees the memory allocated by the streamer itself. 
        */
        virtual void EndEventStream() = 0;
};


