# ======================= Imports =======================
import random
from rdkit import Chem
from rdkit.Chem import rdChemReactions
# ======================= Auxiliar functions =======================
def get_ratio(formulation_dict):
    return {formulation_dict[monomer]['name']:formulation_dict[monomer]['number_molecules_balanced'] for monomer in formulation_dict}
def repeat_monomer(group,available_group):
    new_group=[]
    for t in group:
        i=group.index(t)
        new_group += available_group[i] * [t]
    return new_group
# ======================= Chemical Processes functions =======================
def simple_reaction(rxn,monomer_1,monomer_2):    
    return rxn.RunReactants((monomer_1,monomer_2))[0][0]
def branched_thiol_ene_reaction(balanced):
    #print('\nFormula: ',balanced,'\n')
    generic_thiol_smart = '[SX2H:3]'
    generic_alkene_smart = '[CX3H2:1]=[CX3:2]'
    generic_thioether_smart = '[S:3][C:1][C:2]'
    
    reaction_logs={}

    available_thiols = [balanced[monomer]['number_molecules_balanced'] for monomer in balanced if balanced[monomer]['functional_group']=='thiol']
    available_alkenes = [balanced[monomer]['number_molecules_balanced'] for monomer in balanced if balanced[monomer]['functional_group']=='alkene']

    thiols = [Chem.MolFromSmiles(balanced[monomer]['smiles']) for monomer in balanced if balanced[monomer]['functional_group']=='thiol']
    alkenes = [Chem.MolFromSmiles(balanced[monomer]['smiles']) for monomer in balanced if balanced[monomer]['functional_group']=='alkene']
    
    repeated_thiols = repeat_monomer(thiols,available_thiols)
    repeated_alkenes = repeat_monomer(alkenes,available_alkenes)

    rxn = rdChemReactions.ReactionFromSmarts(f"{generic_thiol_smart}.{generic_alkene_smart}>>{generic_thioether_smart}")

    thiol = repeated_thiols.pop(random.randrange(len(repeated_thiols)))
    alkene = repeated_alkenes.pop(random.randrange(len(repeated_alkenes)))

    molecule = simple_reaction(rxn,thiol,alkene)
    molecule.UpdatePropertyCache()
    reaction_logs[1]=Chem.MolToSmiles(molecule)
    iterations = len(repeated_thiols)+len(repeated_alkenes)

    for _ in range(2,iterations+3):
        if _%2 ==0:
            if len(repeated_alkenes)!=0:
                alkene = repeated_alkenes.pop(random.randrange(len(repeated_alkenes)))
                molecule = simple_reaction(rxn,molecule,alkene)
                molecule.UpdatePropertyCache()
                reaction_logs[_]=Chem.MolToSmiles(molecule)
            elif len(repeated_thiols)!=0:
                thiol = repeated_thiols.pop(random.randrange(len(repeated_thiols)))
                molecule = simple_reaction(rxn,thiol,molecule)
                molecule.UpdatePropertyCache()
                reaction_logs[_]=Chem.MolToSmiles(molecule)
            else:
                break
        elif _%2 !=0:
            if len(repeated_thiols)!=0:
                thiol = repeated_thiols.pop(random.randrange(len(repeated_thiols)))
                molecule = simple_reaction(rxn,thiol,molecule)
                molecule.UpdatePropertyCache()
                reaction_logs[_]=Chem.MolToSmiles(molecule)
            elif len(repeated_alkenes)!=0:
                alkene = repeated_alkenes.pop(random.randrange(len(repeated_alkenes)))
                molecule = simple_reaction(rxn,molecule,alkene)
                molecule.UpdatePropertyCache()
                reaction_logs[_]=Chem.MolToSmiles(molecule)
            else:
                break
    return   Chem.MolToSmiles(molecule)
