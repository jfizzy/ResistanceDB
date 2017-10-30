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

        if not isinstance(intensities, list):
            raise PeakException("Intensities must be a list")

        self._med_mz = med_mz
        self._med_rt = med_rt
        self._compound = compound
        self._category = category
        self._rt_diff = rt_diff
        self._parent = parent
        self._intensities = intensities

    def verify_rt_dif(self, max_rt_dif):
        """ verify that the retention time difference from found peak and expected
            retention time is within the value max_rt_dif """
        return abs(max_rt_dif) > abs(self._rt_diff)

    def verify_instensity_dispartiy(self, disparity):
        """
            verifies that the instensities of the peak have a disparity amongst themselves of
            given parameter 'disparity'. Disparity is expected to be a value between 0 and 1

            Current assumption is that disparity only needs to be found amongst one peak or another
        """

        for i in range(0, len(self.intensities)):
            for j in range(i+1, len(self.intensities)):
                #find smaller intensity
                if self._intensities[i] > self._intensities[j]:
                    smaller_intensity = self._intensities[j]
                    larger_intensity = self._intensities[i]
                else:
                    smaller_intensity = self._intensities[i]
                    larger_intensity = self._intensities[j]

                #divide by larger intensity to see if it is greater than or
                #equal to the required disparity - if so it is valid
                ratio = smaller_intensity / larger_intensity
                if ratio >= disparity:
                    return True

        return False
                    

    ### Getters and Setters ###
    @property
    def intensities(self):
        """ getter for intensities """
        return self._intensities

    @intensities.setter
    def intensities(self, value):
        """ setter for intensities """
        if not isinstance(value, list):
            raise PeakException("Cannot assign a non-list value to property intensities")

        self._parent = value

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
    def rd_diff(self):
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