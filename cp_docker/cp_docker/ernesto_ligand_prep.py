#!/usr/bin/env python
import requests
from subprocess import check_call

from d3r.celppade.custom_ligand_prep import LigandPrep

from config import SMILES_TO_3D_URL, OPENBABEL_CMD

__author__ = 'ocampoernesto@gmail.com'


class LigandPreparation(LigandPrep):
    """Abstract class defining methods for a custom ligand docking solution
    for CELPP
    """
    LigandPrep.OUTPUT_LIG_SUFFIX = '.smi'

    def ligand_scientific_prep(self, 
                               lig_smi_file, 
                               out_lig_file, 
                               targ_info_dict={}):
        """
        Ligand 'scientific preparation' is the process of generating a
        dockable representation of the target ligand from its SMILES
        string.
        :param lig_smi_file: File containing SMILES for target ligand.  
        :param out_lig_file: The result of preparation should have this file name.  
        :param targ_info_dict: A dictionary of information about this target and the candidates chosen for docking.  
        :returns: True if preparation was successful. False otherwise.
        """
        logger.info("converting {} to 3D...".format(lig_smi_file))
        with open(lig_smi_file) as smiles_file:
            smiles_content = smiles_file.read().strip('\n ')

        response = requests.get(SMILES_TO_3D_URL.format(smiles_content))
        if response.status_code != 200:
            raise Exception('Bad response converting to 3D {}'.format(response))

        three_d_content = response.text
        with open(out_lig_file, 'w') as converted_file:
            converted_file.write(three_d_content + '\n')

        logger.info("converted to {}, removing hydrogens...".format(out_lig_file))
        check_call([OPENBABEL_CMD, '-imol2', '-omol2', out_lig_file, '-O{}'.format(out_lig_file), '-d'])
        logger.info("Done with {}".format(out_lig_file))
        return True


if "__main__" == __name__:
    from argparse import ArgumentParser
    import os
    import logging 
    import shutil
    parser = ArgumentParser()
    parser.add_argument("-p", "--pdbdb", metavar="PATH", help="PDB DATABANK which we will dock into")
    parser.add_argument("-c", "--challengedata", metavar="PATH", help="PATH to the unpacked challenge data package")
    parser.add_argument("-o", "--prepdir", metavar="PATH", help="PATH to the output directory")
    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%m/%d/%y %I:%M:%S', filename='final.log',
                        filemode='w', level=logging.INFO)
    opt = parser.parse_args()
    pdb_location = opt.pdbdb
    challenge_data_path = opt.challengedata
    prep_result_path = opt.prepdir

    # running under this dir
    abs_running_dir = os.getcwd()
    log_file_path = os.path.join(abs_running_dir, 'final.log')
    log_file_dest = os.path.join(os.path.abspath(prep_result_path), 'final.log')

    lig_prepper =  LigandPreparation()
    lig_prepper.run_scientific_ligand_prep(challenge_data_path, pdb_location, prep_result_path)

    # move the final log file to the result dir
    shutil.move(log_file_path, log_file_dest)

