# -*- coding: utf-8 -*-

import glob
import os
import fnmatch
import shutil
import sys
import zipfile
import chardet
import re
from unrar import rarfile

def iterfindfiles(path, fnexp):
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

def listfiles(path):
    for i in os.listdir(pathfile):
        fn = os.path.join('%s%s' % (pathfile, i))
        yield fn

def extName(path):
    return os.path.splitext(path)[1]

def unzip(path , fileZipExt):
    # i=0

    for filename in iterfindfiles(path, fileZipExt):
        # i=i+1
        # newfilename = path +str(i) + "_" + os.path.basename(filename)
        newfilename = os.path.basename(filename)
        filesize = os.path.getsize(filename)/1024
        if filesize > 2:
            print filename + "<====>" + newfilename
            print "file size is: %d" %(filesize)
            zfile = zipfile.ZipFile(filename, 'r')
            try:
                for filename in zfile.namelist():
                    zfile.extract(filename, path+"\\unzip")
            except:
                continue
        # shutil.move(filename, newfilename)
        

def unrar(path , fileRarExt):
    # i=0
    for filename in iterfindfiles(path, fileRarExt):
        # i=i+1
        # newfilename = path +str(i) + "_" + os.path.basename(filename)
        try:
            newfilename = os.path.basename(filename)
            filesize = os.path.getsize(filename)/1024
            if filesize > 2:
                print filename + "<====>" + newfilename
                print "file size is: %d" %(filesize)
                
                file = rarfile.RarFile(newfilename)
                file.extractall(path+"\\unzip")
        except:
            continue
        # shutil.move(filename, newfilename)

def fileFilter(path, fileExt):
    unzippath = path+"\\unzip"
    newpath = path+"\\fileFilter"
    for filename in iterfindfiles(unzippath, fileExt):
        fname = os.path.abspath(filename)       
        print fname
        try:
            if os.path.isdir(newpath):
                shutil.copy(fname, newpath)
            else:
                os.mkdir(newpath)
                shutil.copy(fname, newpath)
        except:
            continue

def fileEncoding(filePath):
    f = open(filePath, 'r')
    data = f.read()
    f.close()
    encoding = chardet.detect(data)["encoding"]
    fileExtension = extName(filePath)
    if encoding not in ("UTF-8-SIG", "UTF-16LE", "utf-8", "ascii"):     
        try:
            gb_content = data.decode("gb18030")

            gb_content.encode('utf-8')
            # gb_content.encode('utf-8')
            f = open(filePath, 'w')            
            f.write(gb_content.encode('utf-8'))                  
            f.close()
            
            chSentence(gb_encode, fileExtension)
        except:

            print "except:", filePath
    else:
        
        sentence_set = chSentence(data, fileExtension)
        # path = r"F:\\nltk_work\\SubtitleProject\\SubtitleProject\\result\\final_result\\"
        # srt_filename = path+"srt_result.txt"
        # f = open(srt_filename, 'w')
        # for i in sentence_set:
        #     line = i.encode('utf-8') + "\n"
        #     f.write(line)
        # f.close()
        resultWrite(fileExtension, sentence_set)



def illegalFilter():
    illegal=ur"([\u0000-\u2010]+)"
    pattern_illegals = [re.compile(ur"([\u2000-\u2010]+)"), re.compile(ur"([\u0090-\u0099]+)")]
    filters = ["字幕", "时间轴:", "校对:", "翻译:", "后期:", "监制:"]
    filters.append("时间轴：")
    filters.append("校对：")
    filters.append("翻译：")
    filters.append("后期：")
    filters.append("监制：")
    filters.append("禁止用作任何商业盈利行为")
    filters.append("http")
    htmltagregex = re.compile(r'<[^>]+>',re.S)
    brace_regex = re.compile(r'\{.*\}',re.S)
    slash_regex = re.compile(r'\\\w',re.S)
    repeat_regex = re.compile(r'[-=]{10}',re.S)

    path = r"F:\\nltk_work\\SubtitleProject\\SubtitleProject\\result\\final_result\\"
    filename = path+"result.txt"

    f = open(filename, "r")
    count=0
    while True:
        line = f.readline()
        if line:
            line = line.strip()

            # 编码识别，不是utf-8就过滤
            gb_content = ''
            try:
                gb_content = line.decode("utf-8")
            except Exception as e:
                sys.stderr.write("decode error:  ", line)
                continue

            # 中文识别，不是中文就过滤
            need_continue = False
            for pattern_illegal in pattern_illegals:
                match_illegal = pattern_illegal.findall(gb_content)
                if len(match_illegal) > 0:
                    sys.stderr.write("match_illegal error: %s\n" % line)
                    need_continue = True
                    break
            if need_continue:
                continue

            # 关键词过滤
            need_continue = False
            for filter in filters:
                try:
                    line.index(filter)
                    sys.stderr.write("filter keyword of %s %s\n" % (filter, line))
                    need_continue = True
                    break
                except:
                    pass
            if need_continue:
                continue

            # 去掉剧集信息
            if re.match('.*第.*季.*', line):
                sys.stderr.write("filter copora %s\n" % line)
                continue
            if re.match('.*第.*集.*', line):
                sys.stderr.write("filter copora %s\n" % line)
                continue
            if re.match('.*第.*帧.*', line):
                sys.stderr.write("filter copora %s\n" % line)
                continue

            # 去html标签
            line = htmltagregex.sub('',line)

            # 去花括号修饰
            line = brace_regex.sub('', line)

            # 去转义
            line = slash_regex.sub('', line)

            # 去重复
            new_line = repeat_regex.sub('', line)
            if len(new_line) != len(line):
                continue

            # 去特殊字符
            line = line.replace('-', '').strip()

            if len(line) > 0:
                sys.stdout.write("%s\n" % line)
            count+=1
        else:
            break
    f.close()
    pass


def resultWrite(fileExt, sentence_set):
    path = r"F:\\nltk_work\\SubtitleProject\\SubtitleProject\\result\\final_result\\"
    srt_filename = path+"srt_result.txt"
    ass_filename = path+"ass_result.txt"   
    ssa_filename = path+"ssa_result.txt"       
    result_filename = path+"result.txt"
    if(os.path.isdir(path)):        
        if(fileExt == ".srt"):
            # if os.path.exists(srt_filename):
            #     os.remove(srt_filename)

            srt_file = open(srt_filename, "a+")
            for i in sentence_set:
                line = i.encode('utf-8') + "\n"
                srt_file.write(line)
            srt_file.close()

        if(fileExt == ".ass"):  
            # if os.path.exists(ass_filename):
            #     os.remove(ass_filename)
      
            ass_file = open(ass_filename, "a+")
            for i in sentence_set:
                line = i.encode('utf-8') + "\n"
                ass_file.write(line)
            ass_file.close()

        if(fileExt == ".ssa"):
            # if os.path.exists(ssa_filename): 
            #     os.remove(ssa_filename)

            ssa_file = open(ssa_filename, "a+")
            for i in sentence_set:
                line = i.encode('utf-8') + "\n"
                ssa_file.write(line)
            ssa_file.close()

    else:
        os.mkdir(path)

def chSentence(gbContent, fileExtension):
    cn=ur"([\u4e00-\u9fa5]+)"
    pattern_cn = re.compile(cn)
    jp1=ur"([\u3040-\u309F]+)"
    pattern_jp1 = re.compile(jp1)
    jp2=ur"([\u30A0-\u30FF]+)"
    pattern_jp2 = re.compile(jp2)

    encoding = chardet.detect(gbContent)["encoding"]
    if (fileExtension == ".srt"):
        for sentence in gbContent.decode(encoding).split('\n'):
            try:
                if len(sentence) > 0:
                    match_cn =  pattern_cn.findall(sentence)
                    match_jp1 =  pattern_jp1.findall(sentence)
                    match_jp2 =  pattern_jp2.findall(sentence)
                    sentence = sentence.strip()
                    if len(match_cn)>0 and len(match_jp1)==0 and len(match_jp2) == 0 and len(sentence)>1 and len(sentence.split(' ')) < 10:
                        # print sentence.encode('utf-8')
                        # print sentence
                        final_sentence = sentence
                        yield final_sentence
                        # resultWrite(fileExtension, final_sentence)
            except:
                continue      
    if (fileExtension == ".ass"):
        for line in gbContent.decode(encoding).split('\n'):
            try:
                if line.find('Dialogue') == 0 and len(line) < 500:
                    fields = line.split(',')
                    sentence = fields[len(fields)-1]
                    tag_fields = sentence.split('}')
                    if len(tag_fields) > 1:
                        sentence = tag_fields[len(tag_fields)-1]
                    match_cn =  pattern_cn.findall(sentence)
                    match_jp1 =  pattern_jp1.findall(sentence)
                    match_jp2 =  pattern_jp2.findall(sentence)
                    sentence = sentence.strip()
                    if len(match_cn)>0 and len(match_jp1)==0 and len(match_jp2) == 0 and len(sentence)>1 and len(sentence.split(' ')) < 10:
                        sentence = sentence.replace('\N', '')
                        # print sentence
                        # print sentence.encode('utf-8')
                        # final_sentence = illegalFilter(sentence)
                        # print final_sentence
                        # resultWrite(fileExtension, final_sentence)
                        final_sentence = sentence
                        yield final_sentence

            except:
                continue    

    if (fileExtension == ".ssa"):
        for line in gbContent.decode(encoding).split('\n'):
            try:
                if line.find('Dialogue') == 0 and len(line) < 500:
                    fields = line.split(',')
                    sentence = fields[len(fields)-1]
                    tag_fields = sentence.split('}')
                    if len(tag_fields) > 1:
                        sentence = tag_fields[len(tag_fields)-1]
                    match_cn =  pattern_cn.findall(sentence)
                    match_jp1 =  pattern_jp1.findall(sentence)
                    match_jp2 =  pattern_jp2.findall(sentence)
                    sentence = sentence.strip()
                    if len(match_cn)>0 and len(match_jp1)==0 and len(match_jp2) == 0 and len(sentence)>1 and len(sentence.split(' ')) < 10:
                        sentence = sentence.replace('\N', '')
                        # print sentence
                        # print sentence.encode('utf-8')
                        # final_sentence = illegalFilter(sentence)
                        # resultWrite(fileExtension, final_sentence)
                        final_sentence = sentence
                        yield final_sentence
            except:
                continue    


def combinedFiles():
    path = r"F:\\nltk_work\\SubtitleProject\\SubtitleProject\\result\\final_result\\"
    srt_filename = path+"srt_result.txt"
    ass_filename = path+"ass_result.txt"   
    ssa_filename = path+"ssa_result.txt" 
    result_filename = path+"result.txt"
    try:
        ofile = open(result_filename,'w')
        filelist = [srt_filename, ass_filename, ssa_filename]
        for fr in filelist:
            for text in open(fr, 'r'):
                ofile.write(text)
        ofile.close()
    except:
        pass
    

if __name__ == "__main__":
    path = r"F:\\nltk_work\\SubtitleProject\\SubtitleProject\\result\\"
    fileZipExt = "*.zip"
    fileRarExt = "*.rar"
    fileFilterExt = "*.srt|*.ass|*.ssa"
    # filename = "F:\\nltk_work\\SubtitleProject\\SubtitleProject\\result\\[zmk.tw]maleficent__2014__eng.zip"
    unzip(path, fileZipExt)
    unrar(path, fileRarExt)
    
    fileExt = fileFilterExt.split("|")
    for ext in fileExt:
        try:
            fileFilter(path, ext)
        except:
            continue
    pathfile = path+"\\fileFilter\\"
    for i in listfiles(pathfile):
        try:
            fileEncoding(i)
        except:
            continue

    combinedFiles()


    