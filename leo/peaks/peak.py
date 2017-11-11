""" definitions for the Peak and PeakException class
    a peak defines a single peak found for a specified compound
    among a group of mass spec data files
"""

class Peak:
    """ Defines the characteristics of a peak"""

    def __init__(self, med_mz, med_rt, compound, category, rt_diff, parent, intensities):
        """ Constructor for a peak
        med_mz: molar mass / intensity
        med_rt: Expected retention time
        compound: Name of the compound (expected to be unique)
        category: ?
        rt_diff: Difference in expected retention time vs where the peak was found
        intensities: list of intensities found in samples
        """

        if not isinstance(intensities, dict):
            raise PeakException("Intensities must be a list")

        self._med_mz = med_mz
        self._med_rt = med_rt
        self._compound = compound
        self._category = category
        self._rt_diff = rt_diff
        self._parent = parent
        self._intensities = intensities

    def verify_rt_diff(self, max_rt_dif):
        """ verify that the retention time difference from found peak and expected
            retention time is within the value max_rt_dif """
        return abs(max_rt_dif) > abs(self._rt_diff)

        ## Needs to be rewritten
    def verify_instensity_dispartiy(self, ratio, min_mz):
        """
            verifies that the instensities of the peak have a ratio amongst themselves of
            given parameter 'ratio'. ratio is expected to be a value between 0 and 1
        """
        good_intensities = False

        for organism, _ in self._intensities.items():
            if len(self._intensities[organism]) > 1:
                previous_value = None

                for time, value in self._intensities[organism].items():
                    if not previous_value: 
                        #this is our first iteration, previous value has not been set
                        previous_value = value
                    else:
                        #ensure intensities are above min_mz
                        if previous_value > min_mz or value > min_mz:
                            #if max value is 0, both are 0 - no change.
                            if max(previous_value, value) == 0:
                                continue
                            # if min value is 0 and max value is not 0, 100% change - good sample
                            elif min(previous_value, value) == 0 and max(previous_value, value) != 0:
                                this_dif = 1.0
                                good_intensities = True
                                break
                            # else find ratio between two to find amount of change
                            else:
                                this_dif = 1 - (min(previous_value, value) / max(previous_value, value))
                                #if the ratio between two tests is greater than or equal to ratio passed in - good sample
                                if this_dif >= ratio:
                                    good_intensities = True
                                    break

        return good_intensities

    def __str__(self):
        """ string method """
        return repr("med_mz: {} med_rt: {} compound: {} category: {} rt_diff: {} parent: {} intensities {}".format(\
                self._med_mz, self._med_rt, self._compound, self._category, self._rt_diff, self._parent, self._intensities))

    ### Getters and Setters ###
    @property
    def category(self):
        """ getter for intensities """
        return self._category

    @category.setter
    def category(self, value):
        """ setter for intensities """
        if not isinstance(value, str):
            raise PeakException("Cannot assign a non-list value to property intensities")

        self._category = value

    @property
    def intensities(self):
        """ getter for intensities """
        return self._intensities

    @intensities.setter
    def intensities(self, value):
        """ setter for intensities """
        if not isinstance(value, list):
            raise PeakException("Cannot assign a non-list value to property intensities")

        self._intensities = value

    @property
    def parent(self):
        """ getter for parent """
        return self._parent

    @parent.setter
    def parent(self, value):
        """ setter for parent """
        if not isinstance(value, float):
            raise PeakException("Cannot assign a non-float value to property parent")

        self._parent = value

    @property
    def med_mz(self):
        """ getter for med_mz """
        return self._med_mz

    @med_mz.setter
    def med_mz(self, value):
        """ setter for med_mz """
        if not isinstance(value, float):
            raise PeakException("Cannot assign a non-float value to property med_mz")

        self._med_mz = value

    @property
    def med_rt(self):
        """ getter for med_rt """
        return self._med_rt

    @med_rt.setter
    def med_rt(self, value):
        """ setter for med_rt """
        if not isinstance(value, float):
            raise PeakException("Cannot assign a non-float value to property med_rt")

        self._med_rt = value

    @property
    def rt_diff(self):
        """ getter for rt_diff """
        return self._rt_diff

    @rt_diff.setter
    def rt_diff(self, value):
        """ setter for med_mz """
        if not isinstance(value, float):
            raise PeakException("Cannot assign a non-float value to property rt_diff")

        self._rt_diff = value

    @property
    def compound(self):
        """ getter for compound """
        return self._compound

    @compound.setter
    def compound(self, value):
        """ setter for compound """
        if not isinstance(value, float):
            raise PeakException("Cannot assign a non-string value to property compound")

        self._compound = value


class PeakException(Exception):
    """ Custom exception for Peak class """
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return repr(self._msg)