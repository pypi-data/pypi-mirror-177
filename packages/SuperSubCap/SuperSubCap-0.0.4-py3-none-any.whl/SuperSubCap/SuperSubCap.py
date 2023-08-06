# Version 0.0.3
# Help displays cleaned up and lib tested
# Added sub <-> super translation
# Added caps <-> smalls and help improved

SUMMARY = """%s, library to switch between normal, superscripts, subscripts and caps.
Including greek letters, numbers and basic operands
%s.info() for more info"""%(__name__,__name__)

# For small info
__doc__ = SUMMARY
# help(module_name) or info(module_name) for more infos

alls = ["%s"%(__name__),
        "SUMMARY",
        "alls",
        "help_letters",
        "greek_letters",
        "greek_letters_to_latin",
        "superscripts",
        "superscripts_to_normal",
        "subscripts",
        "subscripts_to_normal",
        "subscripts_to_superscripts",
        "superscripts_to_subscripts",
        "small_to_caps",
        "caps_to_small"]
# 14 elements

# Really detailled informations
def info(*targets:str):
    """info() : get general info about this library
    info(param) : get detailled informations about param
    Parameters: str ==> info about str
    """
    help_letters = {# Content of this library
                    # Library general info
                    "%s"%(__name__):"""Help on module %s:

    %s has %s elements to switch between different letters types:
    Between small and caps, normal to subscripts or superscripts and opposites.
    All letters include latin small and caps and greek small and caps.
    Superscripts and subscripts include numbers and operands.
    info(elem) for more info on elem in %s.alls"""%( __name__, __name__, len(alls)-4,__name__),
                    # SUMMARY
                    "SUMMARY":"""Help on SUMMARY in module %s:

    SUMMARY: summary of this library
    Content of library : alls (list)
    help for all contents of library : help_letters (dict)"""%(__name__),

                    # alls
                    "alls":"""Help on alls in module %s:

    alls: alls[0:3] --> lib info object
    alls: alls[4:%s] --> dict name
    lib info object discribing the contents of this library
    dict name in this file discribing a translation between letter types"""%(len(alls),__name__),
                    
                    # help_letters
                    "help_letters":"""Help on help_letters in module %s:

    help_letters: help_letters[dict] --> documentation for dict
    with dict name contained in alls (list type) 
    Documentation for these dicts for letters - subscripts-superscripts translations"""%(__name__),
                    
                
                # greek_letters
                    "greek_letters":"""Help on greek_letters in module %s:

    greek_letters : latin --> greek
        - Smalls latin
        - Capitals latin
    Ref key latin to greek from https://bailly.app/
    small and capps and var{letter} for variation style
    Feedback to the dev is welcomed"""%(__name__),
                    
                    "greek_letters_to_latin":"""Help on greek_letters_to_latin in module %s:

    greek_letters_to_latin : greek --> latin
        - Smalls greek
        - Capitals greek
    Ref key greek to latin from https://bailly.app/ 
    small and capps available
    Feedback to the dev is welcomed"""%(__name__),
                
                
                # Superscripts
                    "superscripts":"""Help on superscripts in module %s:

    superscripts : normal --> superscript equivalent
        - Numbers and operands
        - Smalls latin
        - Capitals latin
        - Smalls greek
        - Capital greek
    Not all letters have proper equivalent but best is given
    Feedback to the dev is welcomed"""%(__name__),
                    
                    "superscripts_to_normal":"""Help on superscripts_to_normal in module %s:

    superscripts_to_normal : superscript --> normal equivalent
        - Numbers and operands
        - Smalls latin
        - Capitals latin
        - Smalls greek
        - Capital greek
    Not all letters have superscripts equivalent
    so this conversion may not be accurate
    Feedback to the dev is welcomed"""%(__name__),
                
                
                # Subscripts
                    "subscripts":"""Help on subscripts in module %s:

    subscripts: normal --> subscripts equivalent
         - Numbers and operands
         - Smalls latin
         - Capitals latin
         - Smalls greek
         - Capital greek
     Not all letters have subscrips equivalent but best is given
     Feedback to the dev is welcomed"""%(__name__),
                    
                    "subscripts_to_normal":"""Help on subscripts_to_normal in module %s:

    subscripts_to_normal: subscript --> normal
         - Numbers and operands
         - Smalls latin
         - Capitals latin
         - Smalls greek
         - Capital greek
     Not all letters have subscripts equivalent so this conversion 
     may not be accurate
     Feedback to the dev is welcomed"""%(__name__),


                # Subscript to superscript
                "subscripts_to_superscripts":"""Help on subscripts_to_superscripts in module %s:
    subscripts_to_superscripts: subscript --> superscript equivalent
         - Numbers and operands
         - Smalls latin
         - Capitals latin
         - Smalls greek
         - Capital greek
    Not all subscripts have superscripts equivalent but the best is given
    use "varγ" for alternate gamma input
    Feedback to the dev is welcomed"""%(__name__),


                # Superscript to subscript
                "superscripts_to_subscripts":"""Help for superscripts_to_subscripts in module %s:
    superscripts_to_subscripts: superscript --> subscript equivalent
         - Numbers and operands
         - Smalls latin
         - Capitals latin
         - Smalls greek
         - Capital greek
    Not all superscripts have subscripts equivalent but the best is given
    Feedback to the dev is welcomed"""%(__name__),
                # Smalls to caps
                "small_to_caps":"""Help for small_to_caps in module %s:
    small_to_caps : small --> caps equivalent
        - latin
        - Superscripts latin
        - Subscripts latin
        - greek
        - Superscripts greek
        - Subscripts greek
    Not all smalls gave caps equivalent, best is given.
    Feedback to the dev is welcomed"""%(__name__),
                # Caps to smalls 
                "caps_to_small":"""Help on caps_to_small in module %s:
    caps_to_small: caps --> small equivalent
        - Latin
        - Superscripts latin
        - Subscripts latin
        - Greek
        - Superscripts greek
        - Subscripts greek
    Not all caps have smalls equivalent, best if given.
    Feedback to the dev is welcomed"""%(__name__)
                }
    if targets == tuple():
        print(help_letters["%s"%(__name__)])
    for target in targets:
        if target in alls:
            print(help_letters[target],end="\n\n")
        else:
            print(target,"not in",__name__,"module.")
    return None

greek_letters = {# Smalls latin
                 "a":"α","b":"β","varb":"ϐ","c":"ξ","d":"δ","e":"ε","f":"φ","varf":"ϕ","g":"γ",
                 "h":"η","i":"ι","k":"κ","l":"λ","m":"μ","n":"ν","o":"ο","p":"π","q":"θ","varq":"ϑ",
                 "r":"ρ","s":"σ","vars":"ς","t":"τ","u":"υ","v":"ϝ","w":"ω","x":"χ","y":"ψ","z":"ζ",
                 # Capitals latin
                 "A":"Α","B":"Β","C":"Ξ","D":"Δ","E":"Ε","F":"Φ","G":"Γ",
                 "H":"Η","I":"Ι","K":"Κ","L":"Λ","M":"Μ","N":"Ν","O":"Ο","P":"Π","Q":"Θ",
                 "R":"Ρ","S":"Σ","T":"Τ","U":"Υ","V":"Ϝ","W":"Ω","X":"Χ","Y":"Ψ","Z":"Ζ"}

greek_letters_to_latin = {# Smalls greek
                          "α":"a","β":"b","ϐ":"b","ξ":"c","δ":"d","ε":"e","φ":"f","ϕ":"f",
                          "γ":"g","η":"h","ι":"i","κ":"k","λ":"l","μ":"m","ν":"n","ο":"o",
                          "π":"p","θ":"q","ϑ":"q","ρ":"r","σ":"s","ς":"s","τ":"t",
                          "υ":"u","ϝ":"v","ω":"w","χ":"x","ψ":"y","ζ":"z",
                          # Capitals greek
                          "Α":"A","Β":"B","Ξ":"C","Δ":"D","Ε":"E","Φ":"F","Γ":"G",
                          "Η":"H","Ι":"I","Κ":"K","Λ":"L","Μ":"M","Ν":"N","Ο":"O",
                          "Π":"P","Θ":"Q","Ρ":"R","Σ":"S","Τ":"T","Υ":"U","Ϝ":"V",
                          "Ω":"W","Χ":"X","Ψ":"Y","Ζ":"Z",}

superscripts = {# Numbers and operands
              "0":"⁰","1":"¹","2":"²","3":"³","4":"⁴","5":"⁵","6":"⁶","7":"⁷","8":"⁸","9":"⁹",
              "+":"⁺","-":"⁻","=":"⁼","(":"⁽",")":"⁾",
              # Smalls latin
              "a":"ᵃ","b":"ᵇ","c":"ᶜ","d":"ᵈ","e":"ᵉ","f":"ᶠ","g":"ᶢ","h":"ᵸ","i":"ᶦ","j":"ʲ",
              "k":"ᵏ","l":"ˡ","m":"ᵐ","n":"ⁿ","o":"ᵒ","p":"ᵖ","q":"ᑫ","r":"ʳ","s":"ˢ","t":"ᵗ",
              "u":"ᵘ","v":"ᵛ","w":"ʷ","x":"ˣ","y":"ʸ","z":"ᶻ",
              # Capitals latin
              "A":"ᴬ","B":"ᴮ","C":"ᶜ","D":"ᴰ","E":"ᴱ","F":"ᶠ","G":"ᴳ","H":"ᴴ","I":"ⁱ","J":"ᴶ",
              "K":"ᴷ","L":"ᴸ","M":"ᴹ","N":"ᴺ","O":"ᴼ","P":"ᴾ","Q":"ᑫ","R":"ᴿ","S":"ˢ","T":"ᵀ",
              "U":"ᵁ","V":"ⱽ","W":"ᵂ","X":"ˣ","Y":"ʸ","Z":"ᶻ",
              # Smalls greek
              "α":"ᵅ","β":"ᵝ","ϐ":"ᵝ","ξ":"ξ","δ":"ᵟ","ε":"ᵉ","φ":"ᶲ","ϕ":"ᵠ","γ":"ˠ","varγ":"ᵞ",
              "η":"η","ι":"ⁱ","κ":"ᵏ","λ":"λ","μ":"μ","ν":"ᵛ","ο":"ᵒ","π":"π","θ":"θ",
              "ϑ":"ϑ","ρ":"ρ","σ":"σ","ς":"ς","τ":"τ","υ":"ᵘ","ϝ":"ϝ","ω":"ω","χ":"ᵡ",
              "ψ":"ψ","ζ":"ζ",
              # Capital greek
              "Α":"ᴬ","Β":"ᴮ","Ξ":"Ξ","Δ":"ᵟ","Ε":"ᴱ","Φ":"ᶲ","Γ":"ᵞ",
              "Η":"ᴴ","Ι":"ᴵ","Κ":"ᴷ","Λ":"^","Μ":"ᴹ","Ν":"ᴺ","Ο":"ᴼ","Π":"Π","Θ":"Θ",
              "Ρ":"ᴾ","Σ":"Σ","Τ":"ᵀ","Υ":"ʸ","Ϝ":"Ϝ","Ω":"Ω","Χ":"ᵡ","Ψ":"Ψ","Ζ":"ᶻ",
              }

superscripts_to_normal = {# Numbers and operands
                          "⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9",
                          "⁺":"+","⁻":"-","⁼":"=","⁽":"(","⁾":")",
                          # Smalls latin
                          "ᵃ":"a","ᵇ":"b","ᶜ":"c","ᵈ":"d","ᵉ":"e","ᶠ":"f","ᶢ":"g",
                          "ᵸ":"h","ᶦ":"i","ʲ":"j","ᵏ":"k","ˡ":"l","ᵐ":"m","ⁿ":"n",
                          "ᵒ":"o","ᵖ":"p","ᑫ":"q","ʳ":"r","ˢ":"s","ᵗ":"t","ᵘ":"u",
                          "ᵛ":"v","ʷ":"w","ˣ":"x","ʸ":"y","ᶻ":"z",
                          # Capitals latin
                          "ᴬ":"A","ᴮ":"B","ᶜ":"C","ᴰ":"D","ᴱ":"E","ᶠ":"F","ᴳ":"G",
                          "ᴴ":"H","ⁱ":"I","ᴶ":"J","ᴷ":"K","ᴸ":"L","ᴹ":"M","ᴺ":"N",
                          "ᴼ":"O","ᴾ":"P","ᑫ":"Q","ᴿ":"R","ˢ":"S","ᵀ":"T","ᵁ":"U",
                          "ⱽ":"V","ᵂ":"W","ˣ":"X","ʸ":"Y","ᶻ":"Z",
                          # Smalls greek
                          "ᵅ":"α","ᵝ":"β","ᵝ":"ϐ","ξ":"ξ","ᵟ":"δ","ᵉ":"ε","ᶲ":"φ",
                          "ᵠ":"ϕ","ˠ":"γ","ᵞ":"varγ","η":"η","ⁱ":"ι","ᵏ":"κ","λ":"λ",
                          "μ":"μ","ᵛ":"ν","ᵒ":"ο","π":"π","θ":"θ","ϑ":"ϑ","ρ":"ρ",
                          "σ":"σ","ς":"ς","τ":"τ","ᵘ":"υ","ϝ":"ϝ","ω":"ω","ᵡ":"χ",
                          "ψ":"ψ","ζ":"ζ",
                          # Capital greek
                          "ᴬ":"Α","ᴮ":"Β","Ξ":"Ξ","ᵟ":"Δ","ᴱ":"Ε","ᶲ":"Φ","ᵞ":"Γ",
                          "ᴴ":"Η","ᴵ":"Ι","ᴷ":"Κ","^":"Λ","ᴹ":"Μ","ᴺ":"Ν","ᴼ":"Ο",
                          "Π":"Π","Θ":"Θ","ᴾ":"Ρ","Σ":"Σ","ᵀ":"Τ","ʸ":"Υ","Ϝ":"Ϝ",
                          "Ω":"Ω","ᵡ":"Χ","Ψ":"Ψ","ᶻ":"Ζ",}

subscripts = {# Numbers and operands
             "0":"₀","1":"₁","2":"₂","3":"₃","4":"₄","5":"₅","6":"₆","7":"₇","8":"₈","9":"₉",
             "+":"₊","-":"₋","=":"₌","(":"₍",")":"₎",
             # Smalls latin
             "a":"a","b":"b","c":"c","d":"d","e":"ₑ","f":"f","g":"g",
             "h":"ₕ","i":"ᵢ","j":"ⱼ","k":"ₖ","l":"ₗ","m":"ₘ","n":"ₙ",
             "o":"ₒ","p":"ₚ","q":"q","r":"ᵣ","s":"ₛ","t":"ₜ","u":"ᵤ",
             "v":"ᵥ","w":"w","x":"ₓ","y":"y","z":"z",
             # Capitals latin
             "A":"ₐ","B":"ᵦ","C":"𝒸" ,"D":"𝒹" ,"E":"ₑ","F":"𝒻","G":"𝓰",
             "H":"ₕ","I":"ᵢ","J":"ⱼ","K":"ₖ","L":"ₗ","M":"ₘ","N":"ₙ",
             "O":"ₒ","P":"ₚ","Q":"ᵩ","R":"ᵣ","S":"ₛ","T":"ₜ","U":"ᵤ",
             "V":"ᵥ","W":"𝓌","X":"ₓ","Y":"ᵧ","Z":"𝓏",
             # Smalls greek
             "α":"α","β":"ᵦ","ϐ":"ᵦ","ξ":"ξ","δ":"δ","ε":"ε","φ":"ᵩ","ϕ":"ᵩ","γ":"ᵧ","varγ":"ᵧ", # here
             "η":"η","ι":"ι","κ":"ₖ","λ":"λ","μ":"μ","ν":"ᵥ","ο":"ₒ","π":"π","θ":"θ","ϑ":"θ",
             "ρ":"ᵨ","σ":"σ","ς":"ς","τ":"ₜ","υ":"ᵤ","ϝ":"ϝ","ω":"ω","χ":"ᵪ","ψ":"ψ","ζ":"ζ",
             # Capital greek
             "Α":"ₐ","Β":"ᵦ","Ξ":"Ξ","Δ":"Δ","Ε":"ₑ","Φ":"ᵩ","Γ":"ᵧ",
             "Η":"ₕ","Ι":"ᵢ","Κ":"ₖ","Λ":"Λ","Μ":"ₘ","Ν":"ᵥ","Ο":"ₒ","Π":"Π","Θ":"Θ",
             "Ρ":"ᵨ","Σ":"Σ","Τ":"ₜ","Υ":"ᵤ","Ϝ":"Ϝ","Ω":"Ω","Χ":"ᵪ","Ψ":"Ψ","Ζ":"𝓏",
             }

subscripts_to_normal = {# Numbers and operands
                        "₀":"0","₁":"1","₂":"2","₃":"3","₄":"4","₅":"5","₆":"6","₇":"7","₈":"8","₉":"9",
                        "₊":"+","₋":"-","₌":"=","₍":"(","₎":")",
                        # Smalls latin
                        "a":"a","b":"b","c":"c","d":"d","ₑ":"e","f":"f","g":"g",
                        "ₕ":"h","ᵢ":"i","ⱼ":"j","ₖ":"k","ₗ":"l","ₘ":"m","ₙ":"n",
                        "ₒ":"o","ₚ":"p","q":"q","ᵣ":"r","ₛ":"s","ₜ":"t","ᵤ":"u",
                        "ᵥ":"v","w":"w","ₓ":"x","y":"y","z":"z",
                        # Capitals latin (none exist, found replacements)
                        "ₐ":"A","ᵦ":"B","𝒸":"C" ,"𝒹":"D","ₑ":"E","𝒻":"F","𝓰":"G",
                        "ₕ":"H","ᵢ":"I","ⱼ":"J","ₖ":"K","ₗ":"L","ₘ":"M","ₙ":"N",
                        "ₒ":"O","ₚ":"P","ᵩ":"Q","ᵣ":"R","ₛ":"S","ₜ":"T","ᵤ":"U",
                        "ᵥ":"V","𝓌":"W" ,"ₓ":"X","ᵧ":"Y","𝓏":"Z",
                        # Smalls greek
                        "α":"α","ᵦ":"β","ᵦ":"ϐ","ξ":"ξ","δ":"δ","ε":"ε","ᵩ":"φ",
                        "ᵩ":"ϕ","ᵧ":"γ","η":"η","ι":"ι","ₖ":"κ","λ":"λ","μ":"μ","ᵥ":"ν",
                        "ₒ":"ο","π":"π","θ":"θ","θ":"ϑ","ᵨ":"ρ","σ":"σ","ς":"ς",
                        "ₜ":"τ","ᵤ":"υ","ϝ":"ϝ","ω":"ω","ᵪ":"χ","ψ":"ψ","ζ":"ζ",
                        # Capitals Greek
                        "ₐ":"Α","ᵦ":"Β","Ξ":"Ξ","Δ":"Δ","ₑ":"Ε","ᵩ":"Φ","ᵧ":"Γ",
                        "ₕ":"Η","ᵢ":"Ι","ₖ":"Κ","Λ":"Λ","ₘ":"Μ","ᵥ":"Ν","ₒ":"Ο",
                        "Π":"Π","Θ":"Θ","ᵨ":"Ρ","Σ":"Σ","ₜ":"Τ","ᵤ":"Υ","Ϝ":"Ϝ",
                        "Ω":"Ω","ᵪ":"Χ","Ψ":"Ψ","𝓏":"Ζ"}

subscripts_to_superscripts = {# Numbers and operands
                              "₀":"⁰","₁":"¹","₂":"²","₃":"³","₄":"⁴","₅":"⁵","₆":"⁶","₇":"⁷","₈":"⁸","₉":"⁹",
                              "₊":"⁺","₋":"⁻","₌":"⁼","₍":"⁽","₎":"⁾",
                              # Smalls latin
                              "a":"ᵃ","b":"ᵇ","c":"ᶜ","d":"ᵈ","ₑ":"ᵉ","f":"ᶠ","g":"ᶢ",
                              "ₕ":"ᵸ","ᵢ":"ᶦ","ⱼ":"ʲ","ₖ":"ᵏ","ₗ":"ˡ","ₘ":"ᵐ","ₙ":"ⁿ",
                              "ₒ":"ᵒ","ₚ":"ᵖ","q":"ᑫ","ᵣ":"ʳ","ₛ":"ˢ","ₜ":"ᵗ","ᵤ":"ᵘ",
                              "ᵥ":"ᵛ","w":"ʷ","ₓ":"ˣ","y":"ʸ","z":"ᶻ",
                              # Capital latin
                              "ₐ":"ᴬ","ᵦ":"ᴮ","𝒸":"ᶜ","𝒹":"ᴰ" ,"ₑ":"ᴱ","𝒻":"ᶠ" ,"𝓰":"ᴳ",
                              "ₕ":"ᴴ","ᵢ":"ⁱ","ⱼ":"ᴶ","ₖ":"ᴷ","ₗ":"ᴸ","ₘ":"ᴹ","ₙ":"ᴺ",
                              "ₒ":"ᴼ","ₚ":"ᴾ","ᵩ":"ᑫ","ᵣ":"ᴿ","ₛ":"ˢ","ₜ":"ᵀ","ᵤ":"ᵁ",
                              "ᵥ":"ⱽ","𝓌":"ᵂ","ₓ":"ˣ","ᵧ":"ʸ","𝓏":"ᶻ",
                              # Smalls greek
                              "α":"ᵅ","ᵦ":"ᵝ","ᵦ":"ᵝ","ξ":"ξ","δ":"ᵟ","ε":"ᵉ","ᵩ":"ᶲ","ᵩ":"ᵠ",
                              "ᵧ":"ˠ","ᵧ":"ᵞ","η":"η","ι":"ⁱ","ₖ":"ᵏ","λ":"λ","μ":"μ","ᵥ":"ᵛ",
                              "ₒ":"ᵒ","π":"π","θ":"θ","θ":"ϑ","ᵨ":"ρ","σ":"σ","ς":"ς","ₜ":"τ",
                              "ᵤ":"ᵘ","ϝ":"ϝ","ω":"ω","ᵪ":"ᵡ","ψ":"ψ","ζ":"ζ",
                              # Capital greek
                              "ₐ":"ᴬ","ᵦ":"ᴮ","Ξ":"Ξ","Δ":"ᵟ","ₑ":"ᴱ","ᵩ":"ᶲ","ᵧ":"ᵞ","ₕ":"ᴴ",
                              "ᵢ":"ᴵ","ₖ":"ᴷ","Λ":"^","ₘ":"ᴹ","ᵥ":"ᴺ","ₒ":"ᴼ","Π":"Π","Θ":"Θ",
                              "ᵨ":"ᴾ","Σ":"Σ","ₜ":"ᵀ","ᵤ":"ʸ","Ϝ":"Ϝ","Ω":"Ω","ᵪ":"ᵡ","Ψ":"Ψ","𝓏":"ᶻ"}

superscripts_to_subscripts = {# Numbers and operands
                              "⁰":"₀","¹":"₁","²":"₂","³":"₃","⁴":"₄","⁵":"₅","⁶":"₆","⁷":"₇","⁸":"₈","⁹":"₉",
                              "⁺":"₊","⁻":"₋","⁼":"₌","⁽":"₍","⁾":"₎",
                              # Smalls latin
                              "ᵃ":"a","ᵇ":"b","ᶜ":"c","ᵈ":"d","ᵉ":"ₑ","ᶠ":"f","ᶢ":"g",
                              "ᵸ":"ₕ","ᶦ":"ᵢ","ʲ":"ⱼ","ᵏ":"ₖ","ˡ":"ₗ","ᵐ":"ₘ","ⁿ":"ₙ",
                              "ᵒ":"ₒ","ᵖ":"ₚ","ᑫ":"q","ʳ":"ᵣ","ˢ":"ₛ","ᵗ":"ₜ","ᵘ":"ᵤ",
                              "ᵛ":"ᵥ","ʷ":"w","ˣ":"ₓ","ʸ":"y","ᶻ":"z",
                              # Capital latin
                              "ᴬ":"ₐ","ᴮ":"ᵦ","ᶜ":"𝒸","ᴰ":"𝒹" ,"ᴱ":"ₑ","ᶠ":"𝒻","ᴳ":"𝓰",
                              "ᴴ":"ₕ","ⁱ":"ᵢ","ᴶ":"ⱼ","ᴷ":"ₖ","ᴸ":"ₗ","ᴹ":"ₘ","ᴺ":"ₙ",
                              "ᴼ":"ₒ","ᴾ":"ₚ","ᑫ":"ᵩ","ᴿ":"ᵣ","ˢ":"ₛ","ᵀ":"ₜ","ᵁ":"ᵤ",
                              "ⱽ":"ᵥ","ᵂ":"𝓌" ,"ˣ":"ₓ","ʸ":"ᵧ","ᶻ":"𝓏",
                              # Smalls greek
                              "ᵅ":"α","ᵝ":"ᵦ","ᵝ":"ᵦ","ξ":"ξ","ᵟ":"δ","ᵉ":"ε","ᶲ":"ᵩ","ᵠ":"ᵩ",
                              "ˠ":"ᵧ","ᵞ":"ᵧ","η":"η","ⁱ":"ι","ᵏ":"ₖ","λ":"λ","μ":"μ","ᵛ":"ᵥ",
                              "ᵒ":"ₒ","π":"π","θ":"θ","ϑ":"θ","ρ":"ᵨ","σ":"σ","ς":"ς","τ":"ₜ",
                              "ᵘ":"ᵤ","ϝ":"ϝ","ω":"ω","ᵡ":"ᵪ","ψ":"ψ","ζ":"ζ",
                              # Capital greek
                              "ᴬ":"ₐ","ᴮ":"ᵦ","Ξ":"Ξ","ᵟ":"Δ","ᴱ":"ₑ","ᶲ":"ᵩ","ᵞ":"ᵧ","ᴴ":"ₕ",
                              "ᴵ":"ᵢ","ᴷ":"ₖ","^":"Λ","ᴹ":"ₘ","ᴺ":"ᵥ","ᴼ":"ₒ","Π":"Π","Θ":"Θ",
                              "ᴾ":"ᵨ","Σ":"Σ","ᵀ":"ₜ","ʸ":"ᵤ","Ϝ":"Ϝ","Ω":"Ω","ᵡ":"ᵪ","Ψ":"Ψ","ᶻ":"𝓏"}

small_to_caps = {# Latin
                 "a":"A","b":"B","c":"C","d":"D","e":"E","f":"F","g":"G",
                 "h":"H","i":"I","k":"K","l":"L","m":"M","n":"N","o":"O",
                 "p":"P","q":"Q","r":"R","s":"S","t":"T","u":"U","v":"V",
                 "w":"W","x":"X","y":"Y","z":"Z",
                 # Superscripts latin
                 "ᵃ":"ᴬ","ᵇ":"ᴮ","ᶜ":"ᶜ","ᵈ":"ᴰ","ᵉ":"ᴱ","ᶠ":"ᶠ","ᶢ":"ᴳ",
                 "ᵸ":"ᴴ","ᶦ":"ⁱ","ʲ":"ᴶ","ᵏ":"ᴷ","ˡ":"ᴸ","ᵐ":"ᴹ","ⁿ":"ᴺ",
                 "ᵒ":"ᴼ","ᵖ":"ᴾ","ᑫ":"ᑫ","ʳ":"ᴿ","ˢ":"ˢ","ᵗ":"ᵀ","ᵘ":"ᵁ",
                 "ᵛ":"ⱽ","ʷ":"ᵂ","ˣ":"ˣ","ʸ":"ʸ","ᶻ":"ᶻ",
                 # Subscripts latin
                 "a":"ₐ","b":"ᵦ","c":"𝒸","d":"𝒹" ,"ₑ":"ₑ","f":"𝒻","g":"𝓰",
                 "ₕ":"ₕ","ᵢ":"ᵢ","ⱼ":"ⱼ","ₖ":"ₖ","ₗ":"ₗ","ₘ":"ₘ","ₙ":"ₙ","ₒ":"ₒ",
                 "ₚ":"ₚ","q":"ᵩ","ᵣ":"ᵣ","ₛ":"ₛ","ₜ":"ₜ","ᵤ":"ᵤ","ᵥ":"ᵥ","w":"𝓌",
                 "ₓ":"ₓ","y":"ᵧ","z":"𝓏",
                 # Greek
                 "α":"Α","β":"Β","ϐ":"Β","ξ":"Ξ","δ":"Δ","ε":"Ε","φ":"Φ",
                 "ϕ":"Φ","γ":"Γ","η":"Η","ι":"Ι","κ":"Κ","λ":"Λ","μ":"Μ",
                 "ν":"Ν","ο":"Ο","π":"Π","θ":"Θ","ϑ":"Θ","ρ":"Ρ","σ":"Σ",
                 "ς":"Σ","τ":"Τ","υ":"Υ","ϝ":"Ϝ","ω":"Ω","χ":"Χ","ψ":"Ψ","ζ":"Ζ",
                 # Superscripts greek
                 "ᵅ":"ᴬ","ᵝ":"ᴮ","ᵝ":"ᴮ","ξ":"Ξ","ᵟ":"ᵟ","ᵉ":"ᴱ","ᵠ":"ᶲ",
                 "ᶲ":"ᶲ","ˠ":"ᵞ","ᵞ":"ᵞ","η":"ᴴ","ⁱ":"ᴵ","ᵏ":"ᴷ","λ":"^",
                 "μ":"ᴹ","ᵛ":"ᴺ","ᵒ":"ᴼ","π":"Π","θ":"Θ","ϑ":"Θ","ρ":"ᴾ",
                 "σ":"Σ","ς":"Σ","τ":"ᵀ","ᵘ":"ʸ","ϝ":"Ϝ","ω":"Ω","ᵡ":"ᵡ",
                 "ψ":"Ψ","ζ":"ᶻ",
                 # Subscripts greek
                 "α":"ₐ","ᵦ":"ᵦ","ᵦ":"ᵦ","ξ":"Ξ","δ":"Δ","ε":"ₑ","ᵩ":"ᵩ",
                 "ᵧ":"ᵧ","η":"ₕ","ι":"ᵢ","ₖ":"ₖ","λ":"Λ","μ":"ₘ","ᵥ":"ᵥ",
                 "ₒ":"ₒ","π":"Π","θ":"Θ","Θ":"Θ","ᵨ":"ᵨ","σ":"Σ","ς":"Σ",
                 "ₜ":"ₜ","ᵤ":"ᵤ","ϝ":"Ϝ","ω":"Ω","ᵪ":"ᵪ","ψ":"Ψ","ζ":"𝓏",
                 }

caps_to_small = {# Latin
                 "A":"a","B":"b","C":"c","D":"d","E":"e","F":"f","G":"g",
                 "H":"h","I":"i","K":"k","L":"l","M":"m","N":"n","O":"o",
                 "P":"p","Q":"q","R":"r","S":"s","T":"t","U":"u","V":"v",
                 "W":"w","X":"x","Y":"y","Z":"z",
                 # Superscrips latin
                 "ᴬ":"ᵃ","ᴮ":"ᵇ","ᶜ":"ᶜ","ᴰ":"ᵈ","ᴱ":"ᵉ","ᶠ":"ᶠ","ᴳ":"ᶢ",
                 "ᴴ":"ᵸ","ⁱ":"ᶦ","ᴶ":"ʲ","ᴷ":"ᵏ","ᴸ":"ˡ","ᴹ":"ᵐ","ᴺ":"ⁿ",
                 "ᴼ":"ᵒ","ᴾ":"ᵖ","ᑫ":"ᑫ","ᴿ":"ʳ","ˢ":"ˢ","ᵀ":"ᵗ","ᵁ":"ᵘ",
                 "ⱽ":"ᵛ","ᵂ":"ʷ","ˣ":"ˣ","ʸ":"ʸ","ᶻ":"ᶻ",
                 # Subscripts latin
                 "ₐ":"a","ᵦ":"b","𝒸":"c","𝒹":"d","ₑ":"ₑ","𝒻":"f","𝓰":"g",
                 "ₕ":"ₕ","ᵢ":"ᵢ","ⱼ":"ⱼ","ₖ":"ₖ","ₗ":"ₗ","ₘ":"ₘ","ₙ":"ₙ",
                 "ₒ":"ₒ","ₚ":"ₚ","ᵩ":"q","ᵣ":"ᵣ","ₛ":"ₛ","ₜ":"ₜ","ᵤ":"ᵤ",
                 "ᵥ":"ᵥ","𝓌":"w","ₓ":"ₓ","ᵧ":"y","𝓏":"z",
                 # Greek 
                 "Α":"α","Β":"β","Ξ":"ξ","Δ":"δ","Ε":"ε","Φ":"φ","Γ":"γ",
                 "Η":"η","Ι":"ι","Κ":"κ","Λ":"λ","Μ":"μ","Ν":"ν","Ο":"ο",
                 "Π":"π","Θ":"θ","Ρ":"ρ","Σ":"σ","Τ":"τ","Υ":"υ","Ϝ":"ϝ",
                 "Ω":"ω","Χ":"χ","Ψ":"ψ","Ζ":"ζ",
                 # Superscripts greek
                 "ᴬ":"ᵅ","ᴮ":"ᵝ","Ξ":"ξ","ᵟ":"ᵟ","ᴱ":"ᵉ","ᶲ":"ᵠ","ᵞ":"ˠ",
                 "ᴴ":"η","ᴵ":"ⁱ","ᴷ":"ᵏ","^":"λ","ᴹ":"μ","ᴺ":"ᵛ","ᴼ":"ᵒ",
                 "Π":"π","Θ":"θ","ᴾ":"ρ","Σ":"σ","ᵀ":"τ","ʸ":"ᵘ","Ϝ":"ϝ",
                 "Ω":"ω","ᵡ":"ᵡ","Ψ":"ψ","ᶻ":"ζ",
                 # Subscripts greek
                 "ₐ":"α","ᵦ":"ᵦ","Ξ":"ξ","Δ":"δ","ₑ":"ε","ᵩ":"ᵩ","ᵧ":"ᵧ",
                 "ₕ":"η","ᵢ":"ι","ₖ":"ₖ","Λ":"λ","ₘ":"μ","ᵥ":"ᵥ","ₒ":"ₒ",
                 "Π":"π","Θ":"θ","ᵨ":"ᵨ","Σ":"σ","ₜ":"ₜ","ᵤ":"ᵤ","Ϝ":"ϝ",
                 "Ω":"ω","ᵪ":"ᵪ","Ψ":"ψ","𝓏":"ζ"
                 }

# End of library