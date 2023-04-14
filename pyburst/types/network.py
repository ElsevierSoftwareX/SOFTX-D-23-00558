import argparse, shlex
import logging, ROOT

import numpy as np
import pyburst
from .network_cluster import FragmentCluster

logger = logging.getLogger(__name__)


class Network:
    """
    Class to hold information about a network of detectors.

    :param detectors: list of detectors
    :type detectors: list[Detector]
    :param ref_ifo: reference detector
    :type ref_ifo: str
    """

    def __init__(self, config, tf_list, nRMS_list, wdm_MRA=None, silent=False):
        self.net = ROOT.network()
        self.MRA_catalog = None

        if silent:
            # disable logging when network is create for temporary use
            logger.propagate = False
        else:
            logger.propagate = True

        if wdm_MRA:
            # self.MRA_catalog = copy.deepcopy(wdm_MRA)
            # self.net.wdmMRA = self.MRA_catalog.catalog
            self.net.setMRAcatalog(config.MRAcatalog)

        for i, ifo in enumerate(config.ifo):
            self.add_detector(ifo)

        self.load_strains(tf_list, nRMS_list)

        self.update_sky_map(config)

        self.net.constraint(config.delta, config.gamma)
        # net.setDelay(config.refIFO)
        self.net.Edge = config.segEdge
        self.net.netCC = config.netCC
        self.net.netRHO = config.netRHO
        self.net.EFEC = config.EFEC
        self.net.precision = config.precision
        self.net.nSky = config.nSky
        # net.eDisbalance = config.eDisbalance
        self.net.setRunID(0)
        self.net.setAcore(config.Acore)
        self.net.optim = config.optim
        self.net.pattern = config.pattern

        self.update_sky_mask(config)

        self.set_time_shift(config.lagSize, config.lagStep, config.lagOff, config.lagMax,
                            config.lagBuffer, config.lagMode, config.lagSite)

    def load_strains(self, tf_maps, nRMS_list):
        for i in range(self.ifo_size):
            ifo = self.net.getifo(i)
            tf_map = pyburst.conversions.convert_to_wseries(tf_maps[i])
            nRMS = pyburst.conversions.convert_to_wseries(nRMS_list[i])
            ifo.HoT = tf_map
            ifo.TFmap = tf_map
            ifo.nRMS = nRMS

    def set_time_shift(self, lag_size, lag_step, lag_off, lag_max, lag_buffer, lag_mode, lag_site):
        if lag_buffer:
            lags = self.net.setTimeShifts(lag_size, lag_step, lag_off, lag_max, lag_buffer, lag_mode, lag_site)
        else:
            lags = self.net.setTimeShifts(lag_size, lag_step, lag_off, lag_max)
        logger.info("lag step: %s", lag_step)
        logger.info("number of time lags: %s", lags)

    def add_detector(self, detector):
        ifo = ROOT.detector(detector)
        self.net.add(ifo)

    def add_wavelet(self, wavelet):
        self.net.add(wavelet.wavelet)

    def get_ifo(self, ifo):
        return self.net.getifo(ifo)

    def set_veto(self, veto):
        return self.net.setVeto(veto)

    def threshold(self, bpp, alp=None):
        if alp:
            return self.net.THRESHOLD(bpp, alp)
        else:
            return self.net.THRESHOLD(bpp)

    def get_network_pixels(self, lag, threshold):
        self.net.getNetworkPixels(lag, threshold)

        # TODO: return python class?
        # pwc = self.get_cluster(lag)
        # return copy.deepcopy(FragmentCluster().from_netcluster(pwc))

    def cluster(self, lag, kt, kf):
        """
        produce time-frequency clusters at a single TF resolution
        any two pixels are associated if they are closer than both kt/kf
        samples in time/frequency

        :param lag: lag index
        :param kt: time threshold
        :param kf: frequency threshold
        """
        self.get_cluster(lag).cluster(kt, kf)

    def sub_net_cut(self, lag, sub_net, sub_cut, sub_norm):
        return self.net.subNetCut(lag, sub_net, sub_cut, sub_norm, ROOT.nullptr)

    def likelihoodWP(self, mode, lag, search):
        """
        Likelihood analysis with packets

        :param mode: analysis mode
        :type mode: str
        :param lag: lag index
        :param search: if Search = ""/cbc/bbh/imbhb then mchirp is reconstructed
        :return:
        """
        return self.net.likelihoodWP(mode, lag, 0, ROOT.nullptr, search)

    def likelihood2G(self, mode, lag):
        """
        2G likelihood analysis

        :param mode: analysis mode
        :type mode: str
        :param lag: lag index
        :param search: if Search = ""/cbc/bbh/imbhb then mchirp is reconstructed
        :return:
        """
        return self.net.likelihood2G(mode, lag, 0, ROOT.nullptr)

    def get_max_delay(self):
        """
        get the maximum delay between the two detectors

        :return: maximum delay
        :rtype: float
        """
        return self.net.getDelay('MAX')

    def set_delay_index(self, rate):
        self.net.setDelayIndex(rate)

    def get_cluster(self, lag):
        return self.net.getwc(lag)

    @property
    def ifo_size(self):
        return self.net.ifoListSize()

    @property
    def pattern(self):
        return self.net.pattern

    @property
    def nLag(self):
        return self.net.nLag

    @property
    def n_events(self):
        return self.net.events()

    def update_sky_map(self, config, skyres=None):
        """
        Update skymap from configuration, if sky resolution is not specified, use the one in configuration

        :param config: user configuration
        :type config: Config
        :param skyres: sky resolution
        :type skyres: int, optional
        """
        if skyres:
            self.net.setSkyMaps(int(skyres))
        else:
            if config.healpix:
                self.net.setSkyMaps(int(config.healpix))
            else:
                self.net.setSkyMaps(config.angle, config.Theta1, config.Theta2, config.Phi1, config.Phi2)

        self.net.setAntenna()
        self.net.setDelay(config.refIFO)

    def restore_skymap(self, config, skyres=None):
        """
        Restore skymap from configuration, if sky resolution is not specified, use the one in configuration

        :param config: user configuration
        :type config: Config
        :param skyres: sky resolution
        :type skyres: int, optional
        :return: None
        """
        if skyres:
            if config.healpix:
                self.net.setSkyMaps(int(config.healpix))
            else:
                self.net.setSkyMaps(config.angle, config.Theta1, config.Theta2, config.Phi1, config.Phi2)
        self.net.setAntenna()
        self.net.setDelay(config.refIFO)
        if len(config.skyMaskFile) > 0:
            self.set_sky_mask(config, config.skyMaskFile, 'e')
        if len(config.skyMaskCCFile) > 0:
            self.set_sky_mask(config, config.skyMaskCCFile, 'c')

    def update_sky_mask(self, config, skyres: int = None):
        """
        Update sky mask from configuration, if sky resolution is not specified, use the one in configuration

        :param config: user configuration
        :type config: Config
        :param skyres: sky resolution
        :type skyres: int, optional
        """
        if skyres:
            if len(config.skyMaskFile) > 0:
                self.set_sky_mask(config, config.skyMaskFile, 'e', skyres)

            if len(config.skyMaskCCFile) > 0:
                self.set_sky_mask(config, config.skyMaskCCFile, 'c', skyres)

        else:
            if len(config.skyMaskFile) > 0:
                self.set_sky_mask(config, config.skyMaskFile, 'e')

            if len(config.skyMaskCCFile) > 0:
                self.set_sky_mask(config, config.skyMaskCCFile, 'c')

    def set_sky_mask(self, config, options: str, skycoord: str, skyres: float = None):
        """
        set earth/celestial sky mask is used to define what are the sky locations
        that are analyzed by default all sky is used

        option A : \n
        skycoord='e'  \n
          --theta THETA --phi PHI --radius RADIUS \n
          define a circle centered in (THETA,PHI) and radius=RADIUS (THETA : [-90,90], PHI : [0,360], RADIUS : degrees) \n
        skycoord='c' \n
          --theta DEC --phi RA --radius RADIUS \n
          define a circle centered in (DEC,RA) and radius=RADIUS (DEC : [-90,90], RA : [0,360], RADIUS : degrees) \n

        option B: \n
        file name \n
          format : two columns ascii file -> [sky_index	value] \n
          sky_index : is the sky grid index \n
          value     : if !=0 the index sky location is used for the analysis \n

        :param config: Config object
        :param net: network object
        :param options: used to define the earth/celestial SkyMap \n
        :param skycoord: sky coordinates : 'e'=earth, 'c'=celestial
        :param skyres: sky resolution : def=-1 -> use the value defined in parameters (angle,healpix)
        :return:
        """
        if skycoord not in ['e', 'c']:
            raise ValueError("cwb::SetSkyMask - Error : wrong input sky coordinates "
                             " must be 'e'/'c' earth/celestial")

        if options:
            if "--" not in options:  # input parameter is the skyMask file
                if skyres >= 0:
                    return 1
                ret = self.net.setSkyMask(options, skycoord)
                if ret == 0:
                    raise ValueError("cwb::SetSkyMask - Error : skyMask file"
                                     " not exist or it has a wrong format"
                                     " format : two columns ascii file -> [sky_index        value]"
                                     " sky_index : is the sky grid index"
                                     " value     : if !=0 the index sky location is used for the analysis")
                if skycoord == 'e':
                    self.net.setIndexMode(0)
                return 0

            # parse options with python for TB.getParameter(options, "--theta")

            parser = argparse.ArgumentParser(description='Example with long option names')
            parser.add_argument('--theta', default=-1000, type=float)
            parser.add_argument('--phi', default=-1000, type=float)
            parser.add_argument('--radius', default=-1000, type=float)
            args = parser.parse_args(shlex.split('--theta 1 --phi 2 --radius 3'))

            theta = args.theta
            phi = args.phi
            radius = args.radius

            if theta == -1000 or phi == -1000 or radius == -1000:  # input parameter are the skyMask params
                raise ValueError("cwb::SetSkyMask - Error : wrong input skyMask params"
                                 "wrong input options : " + options +
                                 "options must be : --theta THETA --phi PHI --radius RADIUS"
                                 "options must be : --theta DEC --phi AR --radius RADIUS"
                                 "theta must be in the range [-90,90]"
                                 "phi must be in the range [0,360]"
                                 "radius must be > 0")
            else:  # create & set SkyMask
                if skyres < 0:
                    skyres = config.healpix if config.healpix else config.angle
                if config.healpix:
                    SkyMask = ROOT.skymap(int(skyres))
                else:
                    SkyMask = ROOT.skymap(skyres, config.Theta1, config.Theta2, config.Phi1, config.Phi2)
                make_sky_mask(SkyMask, theta, phi, radius)
                self.net.setSkyMask(SkyMask, skycoord)
                if skycoord == 'e':
                    self.net.setIndexMode(0)


def make_sky_mask(sky_mask: ROOT.skymap, theta: float, phi: float, radius: float):
    """
    sky mask is used to define what are the sky locations that are analyzed

    theta,phi,radius are used to define the Celestial SkyMap, define a circle centered in (theta,phi) and radius=radius

    :param sky_mask: output sky celestial mask inside the circle is filled with 1 otherwise with 0
    :type sky_mask: ROOT.skymap
    :param theta: theta, [-90,90]
    :type theta: float
    :param phi: phi, [0,360]
    :type phi: float
    :param radius: radius, degrees
    :type radius: float
    """
    l = sky_mask.size()
    healpix = sky_mask.getOrder()
    # check input parameters
    if abs(theta) > 90 or (phi < 0 or phi > 360) or radius <= 0 or l <= 0:
        raise ValueError("cwb::MakeSkyMask : wrong input parameters !!! "
                         "if(fabs(theta)>90)   cout << theta << \" theta must be in the range [-90,90]\" << endl;"
                         "if(phi<0 || phi>360) cout << phi << \" phi must be in the range [0,360]\" << endl;"
                         "if(radius<=0)        cout << radius << \" radius must be > 0\" << endl;"
                         "if(L<=0)             cout << L << \" SkyMask size must be > 0\" << endl;"
                         "EXIT(1);")

    if not ROOT.gROOT.GetClass("Polar3DVector"):
        ROOT.gSystem.Load("libMathCore")

    # compute the minimun available radius
    # must be greater than the side of a pixel
    if healpix:
        npix = 12 * (int)(4. ** healpix)
        sphere_solid_angle = 4 * np.pi * np.pow(180. / np.pi, 2.)
        skyres = sphere_solid_angle / npix
        if radius < np.sqrt(skyres):
            radius = np.sqrt(skyres)
    else:
        if radius < sky_mask.sms:
            radius = sky_mask.sms
    ph, th = ROOT.GeographicToCwb(phi, theta)
    ov1 = ROOT.Polar3DVector(1, th * np.pi / 180, ph * np.pi / 180)
    nset = 0
    for l in range(l):
        phi = sky_mask.getPhi(l)
        theta = sky_mask.getTheta(l)
        ov2 = ROOT.Polar3DVector(1, theta * np.pi / 180, phi * np.pi / 180)
        dot = ov1.Dot(ov2)
        d_omega = 180 * np.arccos(dot) / np.pi
        if d_omega <= radius:
            sky_mask.set(l, 1)
            nset += 1
        else:
            sky_mask.set(l, 0)
