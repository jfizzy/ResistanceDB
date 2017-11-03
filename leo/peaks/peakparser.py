""" imports: Peak defines a single row designating a peak """
from leo.peaks.peak import Peak
from leo.config.config import Config

class PeakParser():
    """ peak parser  """
    def __init__(self, config):
        """ config: to parse """
        if not isinstance(config, Config):
            raise PeakParserException("Config file must be of type config.Config type object")
        self._config = config

    def parse_peaks(self, peaks):
        """ parses the peaks according to the rules passed in by the config object """
        if peaks and isinstance(peaks[0], Peak):
            bad_peaks = []
            for peak in peaks:
                if not self.validate(peak):
                    bad_peaks.append(peak)

            good_peaks = [pk for pk in peaks if pk not in bad_peaks]
        else:
            raise PeakParserException('Failed to parse peaks. Peaks \
                list must be a non-empty list of Peak type object.')

        return good_peaks

    def validate(self, peak):
        """ validates that a peak conforms to config rules """

        if self.validate_rt_diff(peak, self._config.MAXRTDIFF) \
            and self.validate_min_mz(peak, self._config.MINMZ) \
            and self.validate_mz_ratio(peak, self._config.MZRATIO):
            return True

        return False

    def validate_rt_diff(self, peak, max_rt_diff):
        """ determines if the peak rt_diff is in an acceptable range """
        valid = False
        return valid

    def validate_min_mz(self, peak, min_mz):
        """ determins if the peaks highest mz is above the the min_mz """
        valid = False
        return valid

    def validate_mz_ratio(self, peak, ratio):
        """ determines if the peak has acceptable mz ratios between tests
            A good ratio should show differences between mz values
         """
         valid = False
         return valid

class PeakParserException(Exception):
    """ Custom exception for PeakParser class """
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return repr(self._msg)