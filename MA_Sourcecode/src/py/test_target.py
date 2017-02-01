import os

import baseline_count
import baseline_type
import output_parsing as parsing

import verify_classification as c_verify
import verify_matching as m_verify

import baseline_policies

class Target:
    def __init__(self, name, analysis_script, sourcedir, prefix, ccompiler, cxxcompiler, cc_options, ld_options, binary_path, sourcedir_binary):
        self._name = name
        self._analysis_script = analysis_script
        self._sourcedir = sourcedir
        self._prefix = prefix
        self._ccompiler = ccompiler
        self._cxxcompiler = cxxcompiler
        self._cc_options = cc_options
        self._ld_options = ld_options
        self._binary_path = binary_path
        self._binary_name = os.path.basename(binary_path)
        self._sourcedir_binary = sourcedir_binary

    def name(self):
        return self._name

    def __get_optimizations(self):
        optimizations = []
        #optimizations += ["O0"]
        #optimizations += ["O1"]
        optimizations += ["O2"]
        #optimizations += ["O3"]
        #optimizations += ["Os"]
        return optimizations

    def __do_function_for_all_optimizations(self, function):
        result = {}

        for optimization in self.__get_optimizations():
            result[optimization] = function(optimization)

        return result

    def __do_function_for_all_optimizations2(self, function):
        result = {}

        for optimization in self.__get_optimizations():
            result[optimization] = function(os.path.join(self._prefix, optimization))

        return result

    def __do_function_for_all_optimizations3(self, function):
        result = {}

        for optimization in self.__get_optimizations():
            result[optimization] = function(os.path.join(self._prefix, optimization), self._binary_name)

        return result

    def __do_function_for_all_optimizations3tag(self, function, tag):
        result = {}

        for optimization in self.__get_optimizations():
            result[optimization] = function(os.path.join(self._prefix, optimization), self._binary_name, tag)

        return result

    # <EXTERNAL CALLING FUNCTIONS> 

    # override this!
    def _configure_and_compile(self, prefix, cc_options, ld_options):
        print "Not implemented"

    def _configure_and_compile_opt(self, optimization):
        prefix = os.path.join(self._prefix, optimization)
        cc_options = self._cc_options + " -" + optimization
        return self._configure_and_compile(prefix, cc_options, self._ld_options)

    def configure_and_compile_all(self):
        return self.__do_function_for_all_optimizations(self._configure_and_compile_opt)

    def _analyze(self, prefix):
        # analysis of the "make install" binary
        #command_string = "cd " + prefix + " ; sudo bash " + self._analysis_script + " " + os.path.join(prefix, self._binary_path)
        # analysis of the copy binary (usually the install script has a call to a strip function)
        command_string = "cd " + prefix + " ; sudo bash " + self._analysis_script + " " + os.path.join(prefix, self._binary_name)

        print command_string
        os.system(command_string)

    def analyze_all(self):
        return self.__do_function_for_all_optimizations2(self._analyze)

    # </EXTERNAL CALLING FUNCTIONS>

    # required for svg data, maybe ?
    def _generate_baseline(self, prefix):
        print "_generate_baseline for", prefix

        padyn = parsing.parse_verify(prefix, self._binary_name)
        clang = parsing.parse_x86machine_ground_truth(prefix, self._binary_name)
        count_baseline = baseline_count.generate_cdf_data(clang, padyn)
        type_baseline = baseline_type.generate_cdf_data(clang, padyn)

        return ((count_baseline, type_baseline), "")

    def generate_baseline_all(self):
        return self.__do_function_for_all_optimizations2(self._generate_baseline)

    def _generate_cdf_compare(self, prefix):
        print "_generate_cdf_compare for", prefix

        padyn = parsing.parse_verify(prefix, self._binary_name)
        padyn_type = parsing.parse_type_verify(prefix, self._binary_name)
        clang = parsing.parse_x86machine_ground_truth(prefix, self._binary_name)

        count_baseline = baseline_count.generate_cdf_data(clang, padyn)
        count_real_baseline = baseline_count.generate_cdf_data_real(clang, padyn)
        type_baseline = baseline_type.generate_cdf_data(clang, padyn)
        type_real_baseline = baseline_type.generate_cdf_data_real(clang, padyn_type)

        return ((count_baseline, count_real_baseline, type_baseline, type_real_baseline), "")

    def generate_cdf_compare_all(self):
        return self.__do_function_for_all_optimizations2(self._generate_cdf_compare)

    def generate_policy_baselines_safe_all(self):
        return self.__do_function_for_all_optimizations3(baseline_policies.generate_safe)

    def generate_policy_baselines_conserv_all(self):
        return self.__do_function_for_all_optimizations3(baseline_policies.generate_conserv)

    def generate_policy_baselines_ours_all(self):
        return self.__do_function_for_all_optimizations3(baseline_policies.generate_ours)

    def generate_policy_compare_our_at_all(self):
        return self.__do_function_for_all_optimizations3(baseline_policies.compare_our_at_all)

    def generate_policy_compare_all(self):
        return self.__do_function_for_all_optimizations3(baseline_policies.compare_all)

    def compare_pairing_all(self):
        return self.__do_function_for_all_optimizations3(baseline_policies.compare_count)

#    def compare_pairing_type_all(self):
#        return self.__do_function_for_all_optimizations3(baseline_policies.compare_type)

    def verify_classification_all(self):
        return self.__do_function_for_all_optimizations3(c_verify.verify)

    def verify_classification_ext_all(self, tag):
        return self.__do_function_for_all_optimizations3tag(c_verify.verify_ext, tag)

    def verify_classification_type_ext_all(self, tag):
        return self.__do_function_for_all_optimizations3tag(c_verify.verify_type_ext, tag)

    def verify_classification_type_all(self):
        return self.__do_function_for_all_optimizations3(c_verify.verify_type)

    def verify_classification_type_count_all(self):
        return self.__do_function_for_all_optimizations3(c_verify.verify_type_count)

    def verify_matching_all(self):
        return self.__do_function_for_all_optimizations3(m_verify.verify)


class ConfigMakeTarget(Target):
    def _install(self, prefix):
        command_string = "cp " + os.path.join(self._sourcedir, self._sourcedir_binary, self._binary_name) + " " + os.path.join(prefix, self._binary_name) + ";"
        command_string += "sudo make install"

        print command_string
        os.system(command_string)

    def _configure(self, prefix, cc_options, ld_options):
        command_string = "cd " + self._sourcedir + ";"
        command_string += "sudo make clean; "
        command_string += "CC=\"" + self._ccompiler + "\" "
        command_string += "CXX=\"" + self._cxxcompiler + "\" "
        command_string += "CFLAGS=\"" + cc_options + "\" "
        command_string += "CXXFLAGS=\"" + cc_options + "\" "
        command_string += "LDFLAGS=\"" + ld_options + "\" "
        command_string += "./configure --prefix=\"" + prefix + "\" "
        print command_string
        os.system(command_string)

    def _compile(self, prefix):
        #command_string = "cd " + os.path.join(self._sourcedir, self._sourcedir_binary) + "; "
        #command_string += "make " + self._binary_name +  " 2> " + os.path.join(prefix, "ground_truth." + self._binary_name) + "; "
        command_string = "cd " + self._sourcedir + "; "
        command_string += "make 2> " + os.path.join(prefix, "ground_truth." + self._binary_name) + "; "

        print command_string
        os.system(command_string)

    def _configure_and_compile(self, prefix, cc_options, ld_options):
        if not os.path.exists(prefix):
            os.makedirs(prefix)

        self._configure(prefix, cc_options, ld_options)
        self._compile(prefix)
        self._install(prefix)

class MySQLMakeTarget(ConfigMakeTarget):
    def _compile(self, prefix):
        command_string = "cd " + os.path.join(self._sourcedir, "include") + "; make; "
        command_string += "cd " + os.path.join(self._sourcedir, "vio") + "; make; "
        command_string += "cd " + os.path.join(self._sourcedir, "mysys") + "; make; "
        command_string += "cd " + os.path.join(self._sourcedir, "strings") + "; make; "
        command_string += "cd " + os.path.join(self._sourcedir, "dbug") + "; make; "
        command_string += "cd " + os.path.join(self._sourcedir, "regex") + "; make; "
        command_string += "cd " + os.path.join(self._sourcedir, "storage") + "; make; "
        command_string += "cd " + os.path.join(self._sourcedir, self._sourcedir_binary) + "; "
        command_string += "make gen_lex_hash; "
        command_string += "make " + self._binary_name +  " 2> " + os.path.join(prefix, "ground_truth." + self._binary_name) + "; "

        print command_string
        os.system(command_string)

class LighttpdMakeTarget(ConfigMakeTarget):
    def _compile(self, prefix):
        command_string = "cd " + os.path.join(self._sourcedir, self._sourcedir_binary) + "; "
        command_string += "make versionstamp; "
        command_string += "make " + self._binary_name +  " 2> " + os.path.join(prefix, "ground_truth." + self._binary_name) + "; "

        print command_string
        os.system(command_string)

class PostgreSQLMakeTarget(ConfigMakeTarget):
    def _configure(self, prefix, cc_options, ld_options):
        command_string = "cd " + self._sourcedir + ";"
        command_string += "sudo make clean; "
        command_string += "CC=\"" + self._ccompiler + "\" "
        command_string += "CXX=\"" + self._cxxcompiler + "\" "
        command_string += "CFLAGS=\"" + cc_options + "\" "
        command_string += "CXXFLAGS=\"" + cc_options + "\" "
        command_string += "LDFLAGS=\"" + ld_options + "\" "
        command_string += "./configure --prefix=\"" + prefix + "\" --disable-thread-safety"
        #print command_string
        os.system(command_string)

class NginxMakeTarget(Target):
    #ugly hack not neccessarily needed !
    #def _add_flto_flag(self, makefile_path):
    #    patched_makefile_path = makefile_path + ".patched"
    #    patched_makefile = file(patched_makefile_path, 'w')
    #    with file(makefile_path, 'r') as makefile:
    #        for line in makefile:
    #            if "CFLAGS = " in line:
    #                tokens = line.split("= ")
    #                line = tokens[0] + "= " + "-flto" + tokens[1] 
    #            patched_makefile.write(line)
    #
    #    os.rename(patched_makefile_path, makefile_path)

    def _configure(self, prefix, cc_options, ld_options):
        command_string = "cd " + self._sourcedir + ";"
        command_string += "sudo make clean; "
        command_string += "./configure --prefix=\"" + prefix + "\" "
        command_string += "--with-cc=\"" + self._ccompiler + "\" "
        command_string += "--with-cc-opt=\"" + cc_options + "\" "
        command_string += "--with-ld-opt=\"" + ld_options + "\" "

        #print command_string
        os.system(command_string)

    def _compile(self, prefix):
        command_string = "cd " + self._sourcedir + "; "
        command_string += "make 2> " + os.path.join(prefix, "ground_truth." + self._binary_name)  + "; "

        #print command_string
        os.system(command_string)

    def _install(self, prefix):
        command_string = "cd " + self._sourcedir + ";"
        command_string += "sudo make install;"
        command_string += "cp " + os.path.join(self._sourcedir_binary, self._binary_name) + " " + os.path.join(prefix, self._binary_name)

        #print command_string
        os.system(command_string)

    def _configure_and_compile(self, prefix, cc_options, ld_options):
        if not os.path.exists(prefix):
            os.makedirs(prefix)

        self._configure(prefix, cc_options, ld_options)
        #self._add_flto_flag(self._sourcedir + "/objs/Makefile") # this is nginx specific
        self._compile(prefix)
        self._install(prefix)

class EximMakeTarget(Target):
    def _configure(self, prefix, cc_options, ld_options):
        #TODO: for now no idea how to proceed (perhaps direct makefile patching ?)
        return

    def _compile(self, prefix):
        #TODO: reenable when config works
        #command_string = "cd " + self._sourcedir + "; "
        #command_string += "make install 2> " + os.prefix.join(prefix, "ground_truth." + self._binary_name)
        #
        ##print command_string
        #os.system(command_string)
        return

    def _configure_and_compile(self, prefix, cc_options, ld_options):
        if not os.path.exists(prefix):
            os.makedirs(prefix)

        self._configure(prefix, cc_options, ld_options)
        self._compile(prefix)

class VsftpdMakeTarget(ConfigMakeTarget):

    def __sub_configure(self, prefix, cc_options, ld_options):
        makefile_path = os.path.join(self._sourcedir, "Makefile")
        patched_makefile_path = makefile_path + ".patched"
        patched_makefile = file(patched_makefile_path, 'w')
        with file(makefile_path, 'r') as makefile:
            for line in makefile:
                if line.startswith("CC"):
                    tokens = line.split("=")
                    line = tokens[0] + "=" + self._ccompiler + "\n"
                elif line.startswith("LINK"):
                    tokens = line.split("=")
                    line = tokens[0] + "=" + ld_options + "\n"

                elif line.startswith("LIBS"):
                    tokens = line.split("=")
                    sub_tokens = tokens[1].split(" ")

                    line = tokens[0] + "="

                    if "-ldl" not in sub_tokens:
                        line += " -ldl"

                    if "-lcap" not in sub_tokens:
                        line += " -lcap"

                    if "-lcrypt" not in sub_tokens:
                        line += " -lcrypt"

                    line += tokens[1]

                elif line.startswith("CFLAGS"):
                    tokens = line.split("=")
                    sub_tokens = tokens[1].strip().split(" ")
                    line = tokens[0] + "="
                    for sub_token in sub_tokens:
                        sub_token = sub_token.strip()
                        if sub_token in ["-O0", "-O1", "-O2", "-O3", "-Os"]:
                            sub_token = cc_options
                        if sub_token in ["-flto", "-g"]:
                            sub_token = ""
                        if sub_token != "":
                            line += " " + sub_token
                    line += "\n"
                patched_makefile.write(line)

        os.rename(patched_makefile_path, makefile_path)

    def _configure(self, prefix, cc_options, ld_options):
        self.__sub_configure(prefix, cc_options, ld_options)

        command_string = "cd " + os.path.join(self._sourcedir, self._sourcedir_binary) + "; "
        command_string += "pwd; make clean ; pwd"

        #print command_string
        os.system(command_string)

#    def _compile(self, prefix):
#        command_string = "cd " + self._sourcedir + "; "
#        command_string += "sudo make clean; "
#        command_string += "make 2> " + os.path.join(prefix, "ground_truth." + self._binary_name) + "; "
#        command_string += "mkdir " + os.path.join(prefix, "sbin -p; ")
#        command_string += "cp vsftpd " + os.path.join(prefix, "sbin", "vsftpd; ")
#        command_string += "cp vsftpd " + os.path.join(prefix, "vsftpd")
#
#        print command_string
#        os.system(command_string)

    def _install(self, prefix):
        command_string = "cd " + self._sourcedir + "; "
        command_string += "mkdir " + os.path.join(prefix, "sbin -p; ")
        command_string += "cp vsftpd " + os.path.join(prefix, "sbin", "vsftpd; ")
        command_string += "cp vsftpd " + os.path.join(prefix, "vsftpd")

        #print command_string
        os.system(command_string)

#    def _configure_and_compile(self, prefix, cc_options, ld_options):
#        if not os.path.exists(prefix):
#            os.makedirs(prefix)
#
#        self._configure(prefix, cc_options, ld_options)
#        self._compile(prefix)



class TargetGenerator:
    def __init__(self, analysis_script, prefix, ccompiler, cxxcompiler, cc_options, ld_options):
        self._analysis_script = analysis_script
        self._prefix = prefix
        self._ccompiler = ccompiler
        self._cxxcompiler = cxxcompiler
        self._cc_options = cc_options
        self._ld_options = ld_options

    def generate_target(self, name, sourcedir, method, binary_path, sourcedir_binary):
        analysis_script = self._analysis_script
        prefix = self._prefix
        ccompiler = self._ccompiler
        cxxcompiler = self._cxxcompiler
        cc_options = self._cc_options
        ld_options = self._ld_options

        if name == "exim":
            return EximMakeTarget(name, analysis_script, sourcedir, os.path.join(prefix, name), ccompiler, cxxcompiler, cc_options, ld_options, binary_path, sourcedir_binary)
        elif name == "nginx":
            return NginxMakeTarget(name, analysis_script, sourcedir, os.path.join(prefix, name), ccompiler, cxxcompiler, cc_options, ld_options, binary_path, sourcedir_binary)
        #elif name == "lighttpd":
        #    return LighttpdMakeTarget(name, analysis_script, sourcedir, os.path.join(prefix, name), ccompiler, cxxcompiler, cc_options, ld_options, binary_path, sourcedir_binary)
        elif name == "postgresql":
            return PostgreSQLMakeTarget(name, analysis_script, sourcedir, os.path.join(prefix, name), ccompiler, cxxcompiler, cc_options, ld_options, binary_path, sourcedir_binary)
        #elif name == "mysql":
        #    return MySQLMakeTarget(name, analysis_script, sourcedir, os.path.join(prefix, name), ccompiler, cxxcompiler, cc_options, ld_options, binary_path, sourcedir_binary)
        elif name == "vsftpd":
            return VsftpdMakeTarget(name, analysis_script, sourcedir, os.path.join(prefix, name), ccompiler, cxxcompiler, cc_options, ld_options, binary_path, sourcedir_binary)
        if method == "config+make":
            return ConfigMakeTarget(name, analysis_script, sourcedir, os.path.join(prefix, name), ccompiler, cxxcompiler, cc_options, ld_options, binary_path, sourcedir_binary)
        else:
            return Target(name, analysis_script, sourcedir, os.path.join(prefix, name), ccompiler, cxxcompiler, cc_options, ld_options, binary_path, sourcedir_binary)

