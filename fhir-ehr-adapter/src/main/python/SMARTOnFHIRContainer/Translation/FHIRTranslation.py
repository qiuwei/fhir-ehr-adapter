import json, inspect, collections, xml.etree.ElementTree, sys
from pprint import pprint
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer
import pkgutil
import pyclbr;

#from models.patient import Patient
import models;
import models_full;

from EHR.SystmOne import SystmOne
from Utils.Utilities import Utilities

import importlib;

class FHIRTranslation():
    
    MODELS_PATH = "models_full";
    
    EHR_PATH = "tpp-full";
    
    # Could adjust based on user feedback if, for example, matches are too generous.
    # A user-friendly way of asking about this 'do you feel you've got too many results?'.
    # Different threshold if two words (less strict).
    # Single threshold for all
    TEXT_SIMILARITY_THRESHOLD = 0.95;
    
    SEMANTIC_SIMILARITY_THRESHOLD = 0.8;
    
    GRAMMATICAL_SIMILARITY_THRESHOLD = 0.5;
    
    # Thresholds don't have to be the same at every stage.
    OVERALL_SIMILARITY_THRESHOLD = 0.95;
    
    # Might want to be more generous with child matches.
    OVERALL_CHILD_SIMILARITY_THRESHOLD = 0.8;
    
    # The portion of child fields in an EHR tag that must be housed by a FHIR class in order to consider that class a match.
    CHILD_MATCH_THRESHOLD = 0.5
    
    # If some metrics are too generous (e.g. semantic matching 'address' and 'reference'), then we can reduce their 'contribution' to the measure of similarity using a weighting.
    TEXT_SIMILARITY_WEIGHTING = 1;
    
    SEMANTIC_SIMILARITY_WEIGHTING = 0.8;
    
    GRAMMATICAL_SIMILARITY_WEIGHTING = 0.6;
    
    # Similarity Metric A
    @staticmethod
    def textSimilarity(ehrAttribute, fhirAttribute, stem=True):
        
        # Gradually more complex text similarity
        if ehrAttribute == fhirAttribute:
            return 1.0;
        
        if ehrAttribute.lower() in fhirAttribute.lower():
            return len(ehrAttribute) / float(len(fhirAttribute));
        
        if fhirAttribute.lower() in ehrAttribute.lower():
            return len(fhirAttribute) / float(len(ehrAttribute));
        
        if stem:
            stemmer = PorterStemmer()
            ehrAttribute = stemmer.stem(ehrAttribute);
            fhirAttribute = stemmer.stem(fhirAttribute);
        
        return fuzz.ratio(ehrAttribute, fhirAttribute) / 100.0;
    
    # Similarity Metric B
    @staticmethod
    def semanticSimilarity(ehrAttribute, fhirAttribute):
        
        highestSimilarity = 0;
       
        # wordnet requires word separation by underscore, whereas EHR XML responses (for TPP at least) use camelCase.
        for set in wordnet.synsets(Utilities.capitalToSeparation(ehrAttribute)):
           
            for word in set.lemma_names():
                
                # Get similarity between synonym for ehrAttribute and fhirAttribute. If this is over a given threshold, mark as a semantic match.
                if not word == ehrAttribute and FHIRTranslation.textSimilarity(word, fhirAttribute, True) > highestSimilarity and FHIRTranslation.textSimilarity(word, fhirAttribute, True) > FHIRTranslation.TEXT_SIMILARITY_THRESHOLD:
                    
                    highestSimilarity = FHIRTranslation.textSimilarity(word, fhirAttribute, True);
                    
        return highestSimilarity;    
     
    # Similarity Metric C
    @staticmethod
    def grammaticalSimilarity(ehrAttribute, fhirAttribute):
        
        highestSimilarity = 0;
        
        for lemma in Utilities.lemmas(ehrAttribute):
            
            if FHIRTranslation.textSimilarity(lemma, fhirAttribute, True) > highestSimilarity and FHIRTranslation.textSimilarity(lemma, fhirAttribute, True) > FHIRTranslation.TEXT_SIMILARITY_THRESHOLD:
                
                highestSimilarity = FHIRTranslation.textSimilarity(lemma, fhirAttribute, True);
                    
        return highestSimilarity;
    
    # Similarity Metric D - Sentence progression? e.g. "Done at" and "Location"
    ######
    
    # With highest result False, there needs to be a stricter connection between the class or fields. Probably best for child fields to have stricter match rules.
    @staticmethod
    def compositeStringSimilarity(ehrClassField, fhirClassField, comparisonMethod, highestResult=True):
        
        # If ehrClass string is composite, compare each word with the FHIR target using all of the metrics, and 
        # then use chosen combination method to produce a value.
        # For each word, add these values, and then divide by number of words to get an average match across all words (or max?).
        highestSimilarity = 0;
        totalSimilarity = 0;
        
        ehrWords = Utilities.listFromCapitals(ehrClassField);
        fhirWords = Utilities.listFromCapitals(fhirClassField);
        
        for ehrWord in ehrWords:
            
            highestSimilarityForEHRWord = 0;
            
            for fhirWord in fhirWords:
                
                similarity = comparisonMethod(ehrWord, fhirWord);
                
                if( similarity > highestSimilarity ):
                    
                    highestSimilarity = similarity;
                    
                if ( similarity > highestSimilarityForEHRWord ):
                    
                    highestSimilarityForEHRWord += similarity;
            
            totalSimilarity = highestSimilarityForEHRWord;
            
        if ( highestResult ):
            return highestSimilarity;
        else:
            return totalSimilarity / float(len(ehrWords));
    
    # Return the match value.
    @staticmethod
    def match(ehr, fhir, textSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, semanticSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, grammaticalSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, highestCompositeResult=True):
        
        if (FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.textSimilarity) * FHIRTranslation.TEXT_SIMILARITY_WEIGHTING >= textSimilarityThreshold):
            return FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.textSimilarity, highestCompositeResult);
        elif (FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.semanticSimilarity) * FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING >= semanticSimilarityThreshold):
            return FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.semanticSimilarity, highestCompositeResult);
        elif (FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.grammaticalSimilarity) * FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING >= grammaticalSimilarityThreshold):
            return FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.grammaticalSimilarity, highestCompositeResult);
        else:
            return 0;
    
    # See if there is a match at all, based on thresholds.
    @staticmethod
    def matches(ehr, fhir, textSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, semanticSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, grammaticalSimilarityThreshold=OVERALL_SIMILARITY_THRESHOLD, highestCompositeResult=True):
        
        if (FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.textSimilarity, highestCompositeResult) * FHIRTranslation.TEXT_SIMILARITY_WEIGHTING >= textSimilarityThreshold or 
        FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.semanticSimilarity, highestCompositeResult) * FHIRTranslation.SEMANTIC_SIMILARITY_WEIGHTING >= semanticSimilarityThreshold or 
        FHIRTranslation.compositeStringSimilarity(ehr, fhir, FHIRTranslation.grammaticalSimilarity, highestCompositeResult) * FHIRTranslation.GRAMMATICAL_SIMILARITY_WEIGHTING >= grammaticalSimilarityThreshold):
            return True;
        
        else:
            return False;
    
    @staticmethod
    def getEHRClassChildren(xml, ehrClass):
        return Utilities.getXMLElements(xml.find(".//" + ehrClass), set(), True, True, False, True);
    
    @staticmethod
    def getFHIRClassChildren(fhirClass):
        return Utilities.getFHIRElements(fhirClass, set(), True, True, False);
    
    @staticmethod
    def childSimilarity(ehrClass, fhirClass, ehrClassesToChildren=None, fhirClassesToChildren=None, xml=None):
        
        if ( ehrClassesToChildren ):
            ehrClassChildren = ehrClassesToChildren[ehrClass];
        else:
            ehrClassChildren = FHIRTranslation.getEHRClassChildren(xml, ehrClass);
        
        if ( fhirClassesToChildren ):
            fhirClassChildren = fhirClassesToChildren[fhirClass];  
        else:
            fhirClassChildren = FHIRTranslation.getFHIRClassChildren(fhirClass);
        
        totalChildMatches = 0;
        # Because the number of matches isn't the only thing that's important, it's the accuracy of those matches.
        totalMatchStrength = 0;
        
        if ( fhirClassChildren == None ): return 0;
          
        # For each child of the EHR parent (also includes ATTRIBUTES (same tag) of EHR parent and children).
        for ehrClassChild in ehrClassChildren:
            
            highestMatchStrength = 0;
            hasMatched = False;
            
            # Look at that FHIR classes children
            for fhirClassChild in fhirClassChildren:
                
                # Compare all FHIR class children to each child of this EHR class, and find the most that match in order to resolve multiple potential class matches.
                if FHIRTranslation.matches(ehrClassChild, fhirClassChild, FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, True):
                    
                    matchStrength = FHIRTranslation.match(ehrClassChild, fhirClassChild, FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, False);
                
                    if matchStrength > highestMatchStrength:
                        highestMatchStrength = matchStrength;
                    
                    hasMatched = True;
            
            if hasMatched:
                totalChildMatches += 1;
                
            totalMatchStrength += highestMatchStrength;
        
        if ( totalChildMatches > 0 ):
        
            averageMatchStrength = totalMatchStrength / float(totalChildMatches);
        
            # How many matches have been found for the EHR elements in the candidate FHIR class (weighted by match strength).              
            return (totalChildMatches / float(len(ehrClassChildren))) * averageMatchStrength;   
        
        else:
            return 0;
    
    # Event -> Encounter 
    # Try using content of EHR class to work out FHIR class
    # Input data from multiple EHRs to work out mapping (e.g. Vision has lots more stuff for event).
    
    @staticmethod
    def getFHIRClasses():
        
        fhirClasses = [];
        
        for _, fhirModule, _ in pkgutil.iter_modules([FHIRTranslation.MODELS_PATH]):
            
            # Don't use test modules as a potential match.
            if "_tests" in fhirModule: continue;
             
            for fhirClass in pyclbr.readmodule(FHIRTranslation.MODELS_PATH + "." + fhirModule).keys():
                
                # Import this module as we'll need it later to examine content of FHIR Class
                importedModule = importlib.import_module(FHIRTranslation.MODELS_PATH + "." + fhirModule);
                # Turn the fhirClass string into a fhirClass reference.
                fhirClasses.append(getattr(importedModule, fhirClass));
                
        return fhirClasses;
    
    @staticmethod
    def getPatient(id):
        # return SystmOne().getPatientRecord(id);
        return xml.etree.ElementTree.parse('../../../../resources/' + FHIRTranslation.EHR_PATH + '.xml');
                   
    @staticmethod
    def translatePatient():
        
        #print FHIRTranslation.match("string", "line");
        #print FHIRTranslation.compositeStringSimilarity("CareStartDate", "minValueDate", FHIRTranslation.textSimilarity, True)
        #print FHIRTranslation.matches("Postcode", "PostalCode", FHIRTranslation.OVERALL_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD, FHIRTranslation.OVERALL_CHILD_SIMILARITY_THRESHOLD);
        
        # Try with activitydefinition
        print FHIRTranslation.childSimilarity("Demographics", "models_full.patient.Patient", None, None, FHIRTranslation.getPatient("4917111072"));
        #FHIRTranslation.translatePatientInit();
    
    # Shortest path between two joined concepts in EHR confirms connection in FHIR? E.g. closest mention of 'medication' to 'location' (both are under same XML head in EHR), is 'clinicalimpression' and 'encounter', so these classes are used to hold this information.
    @staticmethod
    def translatePatientInit():
        
        # Get patient record from EHR
        patientXML = FHIRTranslation.getPatient("4917111072");
        
        # Get ehrClasses and fhirClasses
        ehrClasses = Utilities.getXMLElements(patientXML.find("Response"), set(), False);
        fhirClasses = FHIRTranslation.getFHIRClasses();
        
        # Prepare lists of classes and children.
        ehrClassesToChildren = {};
        
        for ehrClass in ehrClasses:
            
            ehrClassesToChildren[ehrClass] = FHIRTranslation.getEHRClassChildren(patientXML, ehrClass);
        
        fhirClassesToChildren = {};
        
        for fhirClass in fhirClasses:
            
            children = FHIRTranslation.getFHIRClassChildren(fhirClass);
            
            if ( children != None ):
                fhirClassesToChildren[fhirClass] = children;
        
        # Remove FHIR classes that do not have children (typically 'type' classes).
        fhirClasses = fhirClassesToChildren.keys();
        
        # Match components of patient record from EHR to components from JSON representation
        
        # Match stage 1: Exact matches
        ehrFHIRMatches = {};
        
        ehrClassesToRemove = set();
        
        for ehrClass in ehrClasses:
        
            matches = 0;
            
            for fhirClass in fhirClasses:
                
                if FHIRTranslation.compositeStringSimilarity(ehrClass, str(fhirClass.__name__), FHIRTranslation.textSimilarity) == 1.0:
                
                    matches += 1;
                    fhirMatch = fhirClass;
            
            # If there is only one 100% match between an EHR Class and FHIR Class, we take this as the best candidate, and remove the EHR class from the pool.
            if matches == 1:
                ehrFHIRMatches[ehrClass] = [(fhirMatch, FHIRTranslation.childSimilarity(ehrClass, fhirMatch, ehrClassesToChildren, fhirClassesToChildren))];
                ehrClassesToRemove.add(ehrClass);
        
        ehrClasses = ehrClasses - ehrClassesToRemove;
        
        # ! NEED TO SEE IF SUBSETS OF XML COULD ALSO MATCH A CLASS, E.G. NAME IN DEMOGRAPHICS IN HUMAN NAME.
        # Extract subset of fields, and if they match a parent field, replace all of those fields with the parent field before performing child match. E.g. replace all name elements in demographics with HumanName match to aid match with patient.
        # These also need to then be counted as matches by the childSimilarity test (e.g. first name, surname, middle name, compiled into human name, adds 3 matches). Although, reducing the number of fields will increase the match strength anyway, as it's over less fields.
        # Only needs to be done with XML elements that do not have children, as these are the fields.
        
        # Match Stage 2: Child matches
        
        # Match EHR to FHIR classes based on similarity between EHR attributes and nested tags and FHIR class attributes.
        for ehrClass in ehrClasses:
            
            ehrFHIRMatches[ehrClass] = [];
            
            childMatches = [];
            
            for fhirClass in fhirClasses:
                
                childSimilarity = FHIRTranslation.childSimilarity(ehrClass, fhirClass, ehrClassesToChildren, fhirClassesToChildren);
                
                childMatches.append((fhirClass, childSimilarity));

            childMatches = sorted(childMatches, key=lambda sortable: (sortable[1]), reverse=True);
            
            for childMatch in childMatches:
                
                if ( childMatch[1] > FHIRTranslation.CHILD_MATCH_THRESHOLD ):
                    ehrFHIRMatches[ehrClass].append(childMatch);
                    
            # If there are no candidates for an ehrClass based on child matches (i.e. none of the matches are above the threshold), then choose the highest.
            if len(ehrFHIRMatches[ehrClass]) == 0:
                
                firstChildMatch = childMatches[0];
                highestMatch = firstChildMatch[1];
                ehrFHIRMatches[ehrClass].append(firstChildMatch);
                
                # Skip the match that has just been added.
                iterChildMatches = iter(childMatches);
                next(iterChildMatches);
                
                for childMatch in iterChildMatches:
                    if ( childMatch[1] == highestMatch ):
                        ehrFHIRMatches[ehrClass].append(childMatch);
                    else:
                        break;
            
        # Match Stage 3: Fuzzy parent matches
        
        # Now decide between multiples matches based upon names of parent classes.
        for ehrClass in ehrFHIRMatches:
            
            # Convert EHR to FHIR class matches to include similarity of parent class names.
            fhirClassChildParentSimilarity = [];
            
            # For each matching FHIR class to this EHR class
            for fhirClassChildSimilarity in ehrFHIRMatches[ehrClass]:
                
                print ehrClass + " " + str(fhirClassChildSimilarity)
                similarity = FHIRTranslation.match(ehrClass, fhirClassChildSimilarity[0].__name__);
                lst = list(fhirClassChildSimilarity)
                # Add the parent similarity to the child similarity to get an overall similarity value.
                lst[1] = lst[1] + similarity;
                fhirClassChildSimilarity = tuple(lst)
                fhirClassChildParentSimilarity.append(fhirClassChildSimilarity);
            
            ehrFHIRMatches[ehrClass] = fhirClassChildParentSimilarity;              
        
        for ehrClass in ehrFHIRMatches:
            
            print ehrClass;
            matches = sorted(ehrFHIRMatches[ehrClass], key=lambda sortable: (sortable[1]), reverse=True);
            
            if len(matches):
                print matches;
        
        # Replace values in JSON version of matching classes.
        # Utilities.getReplaceJSONKeys(patientJSON, None, list(), 'id', 'abc');
        
        # return.
        # return patientJSON
    
    ##########
    
    # Combination Mechanism A
    @staticmethod
    def averageSimilarity(ehrClass, fhirClass):
        
        # Add all similarities together, divide to get between 0 and 1.
        return (FHIRTranslation.textSimilarity(ehrClass, fhirClass, True) + 
                FHIRTranslation.semanticSimilarity(ehrClass, fhirClass) + 
                FHIRTranslation.grammaticalSimilarity(ehrClass, fhirClass)) / 3.0;
        
    # Combination Mechanism B
    @staticmethod
    def maxSimilarity(ehrClass, fhirClass):
        
        return max(FHIRTranslation.textSimilarity(ehrClass, fhirClass, True), 
               max(FHIRTranslation.semanticSimilarity(ehrClass, fhirClass), FHIRTranslation.grammaticalSimilarity(ehrClass, fhirClass)));
    
    ##########
                