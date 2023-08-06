import zeep  # soap 통신에 사용되는 package
import tqdm  # progress bar 표시에 사용되는 package
import os
import zipfile
from datetime import datetime
from multipledispatch import dispatch

class Downloader:
    """
    Baseclass for Mozart zip file download from the server using Mozart OutFileService

    :param url: Mozart server url with port number
    :param subDir: File location to download from the Mozart server
    :example : ml = Downloader('http://192.168.1.2:8000/mozart/OutFileService','VDDF_RTS')

    Methods defined here:
    -- GetFileList() : Return file name list from the server subDir
    -- DownloadFiles(file_list, destination, unzipSwitch=True) : Download Mozart model files for the given file_list to save downloadPath
    -- DownloadFiles(fromDate, toDate, destination, unzipSwitch=True) :Download Mozart model files for the given date period to save downloadPath
    -- DownloadFiles(count, destination, unzipSwitch = True) : Download Mozart model files based on the given number of recently created models

    """
    def __init__(self, url, subDir):
        self.url = '{0}/mex?wsdl'.format(url)
        self.subDir = subDir
        self.client = None
        try:
            self.client = zeep.Client(wsdl=self.url)
        except ConnectionError as error:
            raise Exception('Connection failed. Wrong or inaccessible hostname:'.format(error=error))

    def GetFileList(self):
        """
        Return file name list from the server subDir

        :return: model file list(list<string>)
        """
        files = self.client.service.GetFileList2(self.subDir)
        # with zeep.Client(wsdl=self.url) as client:
        #     files = client.service.GetFileList2(self.subDir)
        return files

    def __checkDir__(self, destination):
        filedir = destination
        if not os.path.exists(filedir):
            print('{0} is not exist path :'.format(filedir))
            pass

    @dispatch(list, str, bool)#for function overloading
    def DownloadFiles(self, file_list, destination, unzipSwitch=True):
        """
        Download Mozart model files for the given file_list to save downloadPath

        :param file_list: model file list to download(list<string>)
        :param destination: local file path to save the downloaded files
        :param unzipSwitch: if true, the zip file is unzipped after downloading
        :return:

        """

        filedir = destination
        if not os.path.exists(filedir):
            raise Exception('{0} is not exist path :'.format(filedir))

        downloadedFiles = []
        for fname in file_list:
            filesize = self.client.service.GetFileSize2(fname, self.subDir)

            offset = 0
            chunkSize = 0x10000  # 10Mbytes
            count = filesize

            progress = tqdm.tqdm(range(filesize), f"Receiving {fname}", unit="B", unit_scale=True,ascii=True,
                                 unit_divisor=1024)
            # progress = tqdm.tqdm(range(filesize), f"Receiving {fname}", ascii=True)

            filePath = os.path.join(filedir, fname)
            with open(filePath, 'wb') as f:
                f.seek(offset, 0)
                while offset < filesize:
                    if filesize >= chunkSize:
                        count = chunkSize
                    buffer = self.client.service.GetFileChunk2(fname, self.subDir, offset, count)
                    if not buffer:
                        break

                    f.write(buffer)
                    offset += len(buffer)
                    progress.update(len(buffer))

                downloadedFiles.append(filePath)
            if unzipSwitch:
                splitFileNames = os.path.splitext(fname)
                if splitFileNames.__len__() < 2:
                    continue
                zipdir = splitFileNames[0]
                if not zipfile.is_zipfile(filePath):
                    continue
                try:
                    with zipfile.ZipFile(filePath,'r') as zip_ref:
                        zip_ref.extractall(os.path.join(filedir, zipdir))
                except ConnectionError as error:
                    print(filePath)
                    print(zipdir)
                    raise error

            progress.close()
        # delete zipfile
        if unzipSwitch:
            for dfile in downloadedFiles:
                os.remove(dfile)

    @dispatch(datetime, datetime, str, bool)#for function overloading
    def DownloadFiles(self, fromDate, toDate, destination, unzipSwitch=True):
        """
        Download Mozart model files for the given date period to save downloadPath

        :param fromDate: Start Date(datetime)
        :param toDate: End Date(datetime)
        :param destination: local file path to save the downloaded files
        :param unzipSwitch: if true, the zip file is unzipped after downloading
        :return:
        """
        filedir = destination
        if not os.path.exists(filedir):
            raise Exception('{0} is not exist path :'.format(filedir))

        files = self.GetFileList()
        if files == None:
            print('There is no data')
            pass

        downloadFiles = []
        for fname in files:
            tmp = os.path.splitext(fname)
            if tmp.__len__() < 2:
                continue

            dateStr = tmp[0][-14:]
            try:
                runTime = datetime.strptime(dateStr, '%Y%m%d%H%M%S')
            except:
                print('{0} cannot recognize date :'.format(fname))
                continue

            if fromDate > runTime or runTime > toDate:
                continue

            downloadFiles.append(fname)
        if downloadFiles.__len__() == 0:
            print('There is no data to download : {0} ~ {1}'.format(fromDate, toDate))
            pass

        self.DownloadFiles(downloadFiles, destination, unzipSwitch)

    @dispatch(int, str, bool)
    def DownloadFiles(self, count, destination, unzipSwitch = True):
        """
        Download Mozart model files based on the given number of recently created models

        :param count: Number of models to download
        :param destination: local file path to save the downloaded files
        :param unzipSwitch: if true, the zip file is unzipped after downloading
        :return:
        """

        self.__checkDir__(destination)

        files = self.GetFileList()

        downloadFiles = []
        chkCnt = 0
        for fname in files:
            if chkCnt == count:
                break
            downloadFiles.append(fname)
            chkCnt += 1

        self.DownloadFiles(downloadFiles, destination, unzipSwitch)




