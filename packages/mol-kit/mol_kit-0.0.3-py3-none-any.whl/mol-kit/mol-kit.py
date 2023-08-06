from rdkit import Chem
from rdkit.Chem import rdDepictor,rdDistGeom
from ase.optimize import LBFGS,FIRE
from ase import Atoms
from pymatgen.io.gaussian import GaussianInput
from pymatgen.core import Molecule
from xtb.ase.calculator import XTB
from pathlib import Path as P
from rich.progress import Progress as Pg
import time,argparse

rdDepictor.SetPreferCoordGen(True)
etkdg = rdDistGeom.ETKDGv3()
etkdg.randomSeed = 0xa700f
etkdg.verbose = False
etkdg.numThreads = 0
etkdg.optimizerForceTol = 0.0135
etkdg.useRandomCoords = False

def readMol(filePath):
    with open(filePath.as_posix(),'r', encoding='unicode_escape') as f:
        molBlock = f.read()
    mol = Chem.MolFromMolBlock(molBlock)
    mol = Chem.AddHs(mol)
    nRBonds = Chem.rdMolDescriptors.CalcNumRotatableBonds(mol)
    hasHeavy = mol.HasSubstructMatch(Chem.MolFromSmarts('* |$M_p$|'))
    return [mol,nRBonds,hasHeavy]

def initAseMol(mol,confId=0):
    symbols=list(map(lambda x:x.GetSymbol(), mol.GetAtoms()))
    conf=mol.GetConformer(confId)
    positions=conf.GetPositions()
    aseMol=Atoms(symbols,positions)
    return aseMol
        
def calculator(aseMol, method="GFNFF", agOp=FIRE, criteria=0.05, steps=100):
    aseMol.calc = XTB(method=method)
    agOp(aseMol).run(fmax = criteria,steps = steps)
    return aseMol

def ase4gauCal(aseMol,rootName,fold,stem):
    symbols = aseMol.get_chemical_symbols()
    coords = aseMol.get_positions()
    gau = GaussianInput(Molecule(symbols, coords),
                        title='s0 opt',
                        dieze_tag='p',
                        functional='b3lyp', 
                        basis_set='6-31g(d)',
                        route_parameters={'opt':'','freq':'','em':'gd3bj'},
                        link0_parameters= {'%mem':'30GB',
                                           '%nprocshared':'32',
                                            '%chk': stem + '.chk'},)
    gau.write_file(P(P.cwd(),rootName,fold,stem+'.gjf'), cart_coords=True)
    
def levelControl(mol,cids,hasHeavy,ag):
    agOp = LBFGS if ag=='LBFGS' else FIRE
    aseList=[]
    if hasHeavy:
        for i in cids:
            aseMol = initAseMol(mol,i)
            aseMol = calculator(aseMol,criteria=0.5,steps=50)
            aseMol = calculator(aseMol,method='GFN2XTB',criteria=0.1,steps=120)
            aseList.append(aseMol)
        energy = list(map(lambda i:i.get_total_energy(), aseList))
        index = energy.index(min(energy))
        aseMol = aseList[index]
    else:
        for i in cids:
            aseMol = initAseMol(mol,i)
            aseMol = calculator(aseMol,criteria=0.5,steps=50)
            aseList.append(aseMol)
        energy = list(map(lambda i:i.get_total_energy(), aseList))
        index = energy.index(min(energy))
        aseMol = aseList[index]
        print('GFN2XTB calculations start:')
        aseMol = calculator(aseMol,method='GFN2XTB',agOp=agOp,criteria=0.1,steps=120)
    return aseMol

def main(weight,ag,inPath,outPath,params=etkdg):
    outFold=time.strftime("%Y%m%d_%H%M%S", time.localtime())
    P(P.cwd(),'out',outFold).mkdir(parents=True,exist_ok=True)
    _molFold = list(P(P.cwd(),inPath).glob('**/*.mol'))
    total_mol=len(_molFold)
    with Pg() as pg:
        taskMain = pg.add_task("[cyan]init setting...", total=total_mol,)
        for ith,molPath in  enumerate(_molFold):
            mol,nRBonds,hasHeavy = readMol(molPath)
            cids = rdDistGeom.EmbedMultipleConfs(mol, numConfs=(weight*nRBonds), params=params)
            pg.update(taskMain,advance=1,description='[cyan]Molecule:[green]{}[red]{:>7}'.format(molPath.stem,str(ith+1)+'/'+str(total_mol)))
            aseMol = levelControl(mol,cids,hasHeavy,ag)
            ase4gauCal(aseMol,outPath,outFold,molPath.stem)
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Conf-kit.py:分子构象搜索输出高斯基态计算文件')
    parser.add_argument('--weight', '-w', help='weight 属性，每个分子的构象采样数量=可转动键*weight',default=3)
    parser.add_argument('--algorithm', '-ag', help='algorithm 属性, 结构优化迭代算法, LBFGS,FIRE', default='FIRE')
    parser.add_argument('--in_path', '-i', help='input_path 属性, 待计算分子的文件夹', default='in')
    parser.add_argument('--out_path', '-o', help='out_path 属性, 结果输出的文件夹', default='out')
    args = parser.parse_args()
    print('-----start conformer calculations:')
    main(weight=args.weight,ag=args.algorithm,inPath=args.in_path,outPath=args.out_path)
    print('-----calculation end.')