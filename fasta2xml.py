import sys

K = int(sys.argv[3])
k = int(sys.argv[4])

with open(sys.argv[2], "w") as f:
    f.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?><beast beautitemplate='snapper' beautistatus='' namespace="beast.core:beast.evolution.alignment:beast.evolution.tree.coalescent:beast.core.util:beast.evolution.nuc:beast.evolution.operators:beast.evolution.sitemodel:beast.evolution.substitutionmodel:beast.base.evolution.alignment:beast.pkgmgmt:beast.base.core:beast.base.inference:beast.base.evolution.tree.coalescent:beast.pkgmgmt:beast.base.core:beast.base.inference.util:beast.evolution.nuc:beast.base.evolution.operator:beast.base.inference.operator:beast.base.evolution.sitemodel:beast.base.evolution.substitutionmodel:beast.base.evolution.likelihood" required="BEAST.base v2.7.3:snapper v1.1.0:SNAPP v1.6.1" version="2.7">
        

    <data
id="dna"
spec="Alignment"
name="rawdata">

""")
    
    taxon2specimen = {}
    seqs = []
    for line in open(sys.argv[1], "r"):
        line = line.split()[0]
        if line[0] == ">":
            if len(seqs) > 0:
                f.write('<sequence id="' + specimen + '_seq" spec="Sequence" taxon="' + specimen + '" totalcount="4" value="' + "".join(seqs) + '"/>\n')
            taxon = line[1:]
            if taxon not in taxon2specimen:
                taxon2specimen[taxon] = []
            specimen = taxon + "_" + str(len(taxon2specimen[taxon]))
            taxon2specimen[taxon].append(specimen)
            seq = ""
            seqs = []
        else:
            seq += line
            if len(seq) >= K:
                seqs.append(line[0:k])
                seq = seq[K:]
    if len(seqs) > 0:
        f.write('<sequence id="' + specimen + '_seq" spec="Sequence" taxon="' + specimen + '" totalcount="4" value="' + "".join(seqs) + '"/>\n')
    f.write("""    </data>



    <map name="Uniform" >beast.base.inference.distribution.Uniform</map>

    

    <map name="Exponential" >beast.base.inference.distribution.Exponential</map>

    

    <map name="LogNormal" >beast.base.inference.distribution.LogNormalDistributionModel</map>

    

    <map name="Normal" >beast.base.inference.distribution.Normal</map>

    

    <map name="Beta" >beast.base.inference.distribution.Beta</map>

    

    <map name="Gamma" >beast.base.inference.distribution.Gamma</map>

    

    <map name="LaplaceDistribution" >beast.base.inference.distribution.LaplaceDistribution</map>

    

    <map name="prior" >beast.base.inference.distribution.Prior</map>

    

    <map name="InverseGamma" >beast.base.inference.distribution.InverseGamma</map>

    

    <map name="OneOnX" >beast.base.inference.distribution.OneOnX</map>

    

    <run id="mcmc" spec="MCMC" chainLength="50000" preBurnin="20000" storeEvery="1000">
            
        <state id="state" spec="State" storeEvery="5000">
                    
            <tree id="Tree.t:dna" spec="beast.base.evolution.tree.Tree" name="stateNode" nodetype="snap.NodeData">
                            
                <taxonset id="TaxonSet.dna" spec="TaxonSet">
                                    
                    <alignment id="snapper.dna" spec="snapper.Data" dataType="integerdata">
                                            
                        <rawdata idref="dna"/>
""")
    for taxon in taxon2specimen:
        f.write('<taxonset id="' + taxon + '" spec="TaxonSet">\n')
        for specimen in taxon2specimen[taxon]:
            f.write('<taxon id="' + specimen + '" spec="Taxon"/>\n')
        f.write('</taxonset>\n\n')
    f.write("""                    </alignment>
                                
                </taxonset>
                        
            </tree>
                    
            <parameter id="snapperCoalescentRate.t:dna" spec="parameter.RealParameter" lower="1.0E-10" name="stateNode" upper="10.0">1.0</parameter>
                    
            <parameter id="bPopSizes.t:dna" spec="parameter.RealParameter" dimension="5" lower="0.0" name="stateNode">380.0</parameter>
                    
            <stateNode id="bGroupSizes.t:dna" spec="parameter.IntegerParameter" dimension="5">1</stateNode>
                    
            <parameter id="parameter.hyperGamma-alpha-SnapperCoalescentRatePrior.t:dna" spec="parameter.RealParameter" name="stateNode">2.0</parameter>
                    
            <parameter id="parameter.hyperGamma-beta-SnapperCoalescentRatePrior.t:dna" spec="parameter.RealParameter" name="stateNode">2.0</parameter>
                
        </state>
            
        <init id="RandomTree.t:dna" spec="RandomTree" estimate="false" initial="@Tree.t:dna" taxa="@snapper.dna">
                    
            <populationModel id="ConstantPopulation0.t:dna" spec="ConstantPopulation">
                            
                <parameter id="randomPopSize.t:dna" spec="parameter.RealParameter" name="popSize">1.0</parameter>
                        
            </populationModel>
                
        </init>
            
        <distribution id="posterior" spec="CompoundDistribution">
                    
            <distribution id="prior" spec="CompoundDistribution">
                            
                <distribution id="BayesianSkyline.t:dna" spec="BayesianSkyline" groupSizes="@bGroupSizes.t:dna" popSizes="@bPopSizes.t:dna">
                                    
                    <treeIntervals id="BSPTreeIntervals.t:dna" spec="beast.base.evolution.tree.TreeIntervals" tree="@Tree.t:dna"/>
                                
                </distribution>
                            
                <distribution id="MarkovChainedPopSizes.t:dna" spec="distribution.MarkovChainDistribution" jeffreys="true" parameter="@bPopSizes.t:dna"/>
                            
                <prior id="HyperPrior.hyperGamma-alpha-SnapperCoalescentRatePrior.t:dna" name="distribution" x="@parameter.hyperGamma-alpha-SnapperCoalescentRatePrior.t:dna">
                                    
                    <OneOnX id="OneOnX.4" name="distr"/>
                                
                </prior>
                            
                <prior id="HyperPrior.hyperGamma-beta-SnapperCoalescentRatePrior.t:dna" name="distribution" x="@parameter.hyperGamma-beta-SnapperCoalescentRatePrior.t:dna">
                                    
                    <OneOnX id="OneOnX.5" name="distr"/>
                                
                </prior>
                            
                <prior id="SnapperCoalescentRatePrior.t:dna" name="distribution" x="@snapperCoalescentRate.t:dna">
                                    
                    <Gamma id="Gamma.14" alpha="@parameter.hyperGamma-alpha-SnapperCoalescentRatePrior.t:dna" beta="@parameter.hyperGamma-beta-SnapperCoalescentRatePrior.t:dna" name="distr"/>
                                
                </prior>
                        
            </distribution>
                    
            <distribution id="likelihood" spec="CompoundDistribution" useThreads="true">
                            
                <distribution id="snapperTreeLikelihood.dna" spec="snapper.SnapperTreeLikelihood" data="@snapper.dna" pattern="coalescentRate" tree="@Tree.t:dna">
                                    
                    <siteModel id="SnapperSiteModel.s:dna" spec="SiteModel">
                                            
                        <substModel id="SnapperSubstModel.s:dna" spec="snapper.SnapSubstitutionModel" coalescentRate="@snapperCoalescentRate.t:dna">
                                                    
                            <parameter id="snapperU.s:dna" spec="parameter.RealParameter" estimate="false" lower="0.0" name="mutationRateU">1.0</parameter>
                                                    
                            <parameter id="snapperV.s:dna" spec="parameter.RealParameter" estimate="false" lower="0.0" name="mutationRateV">1.0</parameter>
                                                
                        </substModel>
                                        
                    </siteModel>
                                    
                    <branchRateModel id="StrictClock.c:dna" spec="beast.base.evolution.branchratemodel.StrictClockModel">
                                            
                        <parameter id="clockRate.c:dna" spec="parameter.RealParameter" estimate="false" name="clock.rate">1.0</parameter>
                                        
                    </branchRateModel>
                                
                </distribution>
                        
            </distribution>
                
        </distribution>
            
        <operator id="SnapperGammaMover.t:dna" spec="snap.operators.GammaMover" coalescenceRate="@snapperCoalescentRate.t:dna" scale="0.75" weight="1.0"/>
            
        <operator id="SnapperRateMixer.t:dna" spec="snap.operators.RateMixer" coalescenceRate="@snapperCoalescentRate.t:dna" scaleFactors="0.25" tree="@Tree.t:dna" weight="1.0"/>
            
        <operator id="BayesianSkylineBICEPSEpochTop.t:dna" spec="EpochFlexOperator" scaleFactor="0.1" tree="@Tree.t:dna" weight="2.0"/>
            
        <operator id="BayesianSkylineBICEPSEpochAll.t:dna" spec="EpochFlexOperator" fromOldestTipOnly="false" scaleFactor="0.1" tree="@Tree.t:dna" weight="2.0"/>
            
        <operator id="BayesianSkylineBICEPSTreeFlex.t:dna" spec="TreeStretchOperator" scaleFactor="0.01" tree="@Tree.t:dna" weight="2.0"/>
            
        <operator id="BayesianSkylineTreeRootScaler.t:dna" spec="kernel.BactrianScaleOperator" rootOnly="true" scaleFactor="0.1" tree="@Tree.t:dna" upper="10.0" weight="3.0"/>
            
        <operator id="BayesianSkylineUniformOperator.t:dna" spec="kernel.BactrianNodeOperator" tree="@Tree.t:dna" weight="30.0"/>
            
        <operator id="BayesianSkylineSubtreeSlide.t:dna" spec="kernel.BactrianSubtreeSlide" tree="@Tree.t:dna" weight="15.0"/>
            
        <operator id="BayesianSkylineNarrow.t:dna" spec="Exchange" tree="@Tree.t:dna" weight="0.0"/>
            
        <operator id="BayesianSkylineWide.t:dna" spec="Exchange" isNarrow="false" tree="@Tree.t:dna" weight="3.0"/>
            
        <operator id="BayesianSkylineWilsonBalding.t:dna" spec="WilsonBalding" tree="@Tree.t:dna" weight="3.0"/>
            
        <operator id="popSizesScaler.t:dna" spec="kernel.BactrianScaleOperator" parameter="@bPopSizes.t:dna" upper="10.0" weight="15.0"/>
            
        <operator id="groupSizesDelta.t:dna" spec="operator.kernel.BactrianDeltaExchangeOperator" integer="true" weight="6.0">
                    
            <intparameter idref="bGroupSizes.t:dna"/>
                
        </operator>
            
        <operator id="hyperScaler.hyperGamma-alpha-SnapperCoalescentRatePrior.t:dna" spec="ScaleOperator" parameter="@parameter.hyperGamma-alpha-SnapperCoalescentRatePrior.t:dna" scaleFactor="0.5" weight="0.1"/>
            
        <operator id="hyperScaler.hyperGamma-beta-SnapperCoalescentRatePrior.t:dna" spec="ScaleOperator" parameter="@parameter.hyperGamma-beta-SnapperCoalescentRatePrior.t:dna" scaleFactor="0.5" weight="0.1"/>
            
        <logger id="tracelog" spec="Logger" fileName="$(filebase).log" logEvery="1000" model="@posterior" sanitiseHeaders="true" sort="smart">
                    
            <log idref="posterior"/>
                    
            <log idref="likelihood"/>
                    
            <log idref="prior"/>
                    
            <log id="TreeHeight.t:dna" spec="beast.base.evolution.tree.TreeStatLogger" tree="@Tree.t:dna"/>
                    
            <log idref="snapperCoalescentRate.t:dna"/>
                    
            <log idref="BayesianSkyline.t:dna"/>
                    
            <log idref="bPopSizes.t:dna"/>
                    
            <log idref="bGroupSizes.t:dna"/>
                    
            <log idref="parameter.hyperGamma-alpha-SnapperCoalescentRatePrior.t:dna"/>
                    
            <log idref="HyperPrior.hyperGamma-alpha-SnapperCoalescentRatePrior.t:dna"/>
                    
            <log idref="parameter.hyperGamma-beta-SnapperCoalescentRatePrior.t:dna"/>
                    
            <log idref="HyperPrior.hyperGamma-beta-SnapperCoalescentRatePrior.t:dna"/>
                
        </logger>
            
        <logger id="screenlog" spec="Logger" logEvery="1000">
                    
            <log idref="posterior"/>
                    
            <log idref="likelihood"/>
                    
            <log idref="prior"/>
                
        </logger>
            
        <logger id="treelog.t:dna" spec="Logger" fileName="$(filebase).trees" logEvery="1000" mode="tree">
                    
            <log id="TreeWithMetaDataLogger.t:dna" spec="beast.base.evolution.TreeWithMetaDataLogger" tree="@Tree.t:dna"/>
                
        </logger>
        
    </run>
</beast>
""")
