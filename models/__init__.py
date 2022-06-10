import json
from datetime import datetime
from enum import Enum

from conftest import ORACLE_SCHEMA

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.oracle import CLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Base.metadata.schema = ORACLE_SCHEMA


class Permission(str, Enum):
    NONE = "NONE"
    MEMBER = "MEMBER"
    ADMIN = "ADMIN"


class KeywordType(str, Enum):
    ALL = "ALL"
    KEY = "KEY"
    VALUE = "VALUE"


class ServiceType(str, Enum):
    OCR = "OCR"
    NLP = "NLP"


class NLPResultStatus(str, Enum):
    WAITING = "WAITING"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    CONFIRM = "CONFIRM"


class RequestStatus(str, Enum):
    Analyse_Waiting = "WAITING"
    Analyse_Completed = "SUCCESS"
    Analyse_Failed = "FAIL"
    Confirm_Completed = "CONFIRM"


class RequestFrom(str, Enum):
    ADMIN = "ADMIN"
    AGENT = "AGENT"


class FileStatus(str, Enum):
    WAITING = "WAITING"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


class FileStep(str, Enum):
    ## 병합 ##
    Before_File_Merging = "Before_File_Merging"
    File_Merge_Completed = "File_Merge_Completed"

    ## 업로드 ##
    Upload_Waiting = "Upload_Waiting"
    Upload_Completed = "Upload_Completed"

    ## OCR ##
    OCR_Completed = "OCR_Completed"

    ## NLP ##
    Analyse_Completed = "Analyse_Completed"

    ## 검수 ##
    Confirm_Processing = "Confirm_Processing"
    Confirm_Completed = "Confirm_Completed"

    SEQ = [Upload_Waiting, Upload_Completed, OCR_Completed, Analyse_Completed]
    FILE_SUCCESS = [Upload_Completed, OCR_Completed, Analyse_Completed]
    OCR_SUCCESS = [OCR_Completed, Analyse_Completed]
    CONFIRM_STATUS = [Confirm_Completed]
    SUCCESS_STATUS = [Analyse_Completed, Confirm_Processing, Confirm_Completed]


class ReqError(str, Enum):
    All_Failed = "ALL Failed"
    Contract_Failed = "Contract Failed"


class FileError(str, Enum):
    ### Error ###
    Analyse_Stopping = "Analyse Stopping Error"
    Analyse_Stopped = "Analyse Stopped Error"

    OCR_Failed = "OCR Error"
    NLP_Failed = "NLP Error"
    FILE_Failed = "File Error"

    DB_Failed = "DB Error"
    SYS_Failed = "System Error"

    Merge_Failed = "Merge Error"
    Extension_error = "Extension Error"
    IMG_system_error = "IMG System Error"

    NLP_Connection_Error = "NLP Connection Error"
    Admin_Error = "Admin Error"
    OCR_Error = "OCR Error"
    Classifier_Error = "Classifier Error"
    NER_Error = "NER Error"
    Spell_checker_Error = "Spell_checker Error"
    IMG_package_Error = "IMG_package Error"
    Template_Error = "Template Error"
    Mapper_Error = "Mapper Error"
    Postprocessor_Error = "Postprocessor Error"
    Keyword_searcher_Error = "Keyword_searcher Error"
    File_Not_Found_Error = "File Not Found Error"
    NLP_System_Error = "NLP System Error"
    Damaged_File_Error = "Damaged File Error"

    Confirmed_Check_List = [
        OCR_Failed,
        NLP_Failed,
        FILE_Failed,
        DB_Failed,
        SYS_Failed,
        Merge_Failed,
        Extension_error,
        IMG_system_error,
    ]

    ERRORS_ALL = [
        Analyse_Stopping,
        Analyse_Stopped,
        OCR_Failed,
        NLP_Failed,
        FILE_Failed,
        DB_Failed,
    ]


class OCRNLPSteps(str, Enum):
    FILE_MERGE = "FILE MERGE"
    FILE_PROCESS = "FILE PROCESS"
    OCR_PROCESS = "OCR PROCESS"
    NLP_PROCESS = "NLP PROCESS"
    SEQ = [None, FILE_PROCESS, OCR_PROCESS, NLP_PROCESS]


class NLPErrorStep(Enum):
    NLP_Error = "NLP Error"
    NLP_Connection_Error = "NLP Connection Error"
    Admin_Error = "Admin Error"
    OCR_Error = "OCR Error"
    Classifier_Error = "Classifier Error"
    NER_Error = "NER Error"
    Spell_checker_Error = "Spell_checker Error"
    IMG_package_Error = "IMG_package Error"
    Template_Error = "Template Error"
    Mapper_Error = "Mapper Error"
    Postprocessor_Error = "Postprocessor Error"
    Keyword_searcher_Error = "Keyword_searcher Error"
    File_Not_Found_Error = "File Not Found Error"
    NLP_System_Error = "NLP System Error"

    Error_Step = [
        NLP_Error,
        NLP_Connection_Error,
        Admin_Error,
        OCR_Error,
        Classifier_Error,
        NER_Error,
        Spell_checker_Error,
        IMG_package_Error,
        Template_Error,
        Mapper_Error,
        Postprocessor_Error,
        Keyword_searcher_Error,
        File_Not_Found_Error,
        NLP_System_Error,
    ]


class User(Base):
    __tablename__ = "admin_user"

    user_id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_name: str = Column(String(32))
    user_account: str = Column(String(32), unique=True)
    password: str = Column(String(128))
    is_super: bool = Column(Boolean, default=False, index=True)
    admin_permission: str = Column(String(8), default=Permission.MEMBER, index=True)
    review_permission: bool = Column(Boolean, default=True, index=True)
    is_active: bool = Column(Boolean, default=True, index=True)
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(DateTime(timezone=True))
    last_login_date: datetime = Column(DateTime(timezone=True))
    pwd_updated_date: datetime = Column(DateTime(timezone=True), default=func.now())
    ip_list: str = Column(String(4000), default=json.dumps("[]"))


class Business(Base):
    __tablename__ = "admin_business"

    biz_id: int = Column(Integer, primary_key=True, autoincrement=True)
    biz_code: str = Column(String(32))
    biz_name: str = Column(String(64))
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )


class Task(Base):
    __tablename__ = "admin_task"

    task_id: int = Column(Integer, primary_key=True, autoincrement=True)
    task_code: str = Column(String(32))
    task_name: str = Column(String(64))
    biz_id: int = Column(
        Integer, ForeignKey("admin_business.biz_id", ondelete="CASCADE"), index=True
    )
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )


class Document(Base):
    __tablename__ = "admin_document"

    doc_id: int = Column(Integer, primary_key=True, autoincrement=True)
    doc_code: str = Column(String(32))
    doc_name: str = Column(String(128))
    extraction_target: str = Column(String(8), index=True)
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )


class DocumentByTask(Base):
    __tablename__ = "admin_document_by_task"

    doc_by_task_id: int = Column(Integer, primary_key=True, autoincrement=True)
    task_id: int = Column(
        Integer, ForeignKey("admin_task.task_id", ondelete="CASCADE"), index=True
    )
    doc_id: int = Column(
        Integer, ForeignKey("admin_document.doc_id", ondelete="CASCADE"), index=True
    )


class ItemType(Base):
    __tablename__ = "admin_item_type"

    item_type_id: int = Column(Integer, primary_key=True, autoincrement=True)
    item_type_name: str = Column(String(64))
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )


class Meta(Base):
    __tablename__ = "admin_meta"

    meta_id: int = Column(Integer, primary_key=True, autoincrement=True)
    meta_name: str = Column(String(64))
    item_type_id: int = Column(
        Integer,
        ForeignKey("admin_item_type.item_type_id", ondelete="SET NULL"),
        index=True,
    )
    depth: str = Column(String(16))
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )


class Item(Base):
    __tablename__ = "admin_item"

    item_id: int = Column(Integer, primary_key=True, autoincrement=True)
    item_name: str = Column(String(128))
    meta_id: int = Column(Integer, ForeignKey("admin_meta.meta_id"), index=True)
    priority: int = Column(Integer)
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )
    doc_id: int = Column(
        Integer, ForeignKey("admin_document.doc_id", ondelete="CASCADE"), index=True
    )


class ItemByTask(Base):
    __tablename__ = "admin_item_by_task"

    item_by_task_id: int = Column(Integer, primary_key=True, autoincrement=True)
    item_id: int = Column(
        Integer, ForeignKey("admin_item.item_id", ondelete="CASCADE"), index=True
    )
    task_id: int = Column(
        Integer, ForeignKey("admin_task.task_id", ondelete="CASCADE"), index=True
    )
    meta_id: int = Column(
        Integer, ForeignKey("admin_meta.meta_id", ondelete="SET NULL"), index=True
    )
    priority: int = Column(Integer)
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )


class Category(Base):
    __tablename__ = "admin_category"

    category_id: int = Column(Integer, primary_key=True, autoincrement=True)
    category_name: str = Column(String(128))
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )


class Keyword(Base):
    __tablename__ = "admin_keyword"

    keyword_id: int = Column(Integer, primary_key=True, autoincrement=True)
    keyword_name: str = Column(String(4000))
    category_id: int = Column(
        Integer,
        ForeignKey("admin_category.category_id", ondelete="SET NULL"),
        index=True,
    )
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )
    doc_id: int = Column(
        Integer, ForeignKey("admin_document.doc_id", ondelete="CASCADE"), index=True
    )


class KeywordByTask(Base):
    __tablename__ = "admin_keyword_by_task"

    keyword_by_task_id: int = Column(Integer, primary_key=True, autoincrement=True)
    keyword_id: int = Column(
        Integer, ForeignKey("admin_keyword.keyword_id", ondelete="CASCADE"), index=True
    )
    task_id: int = Column(
        Integer, ForeignKey("admin_task.task_id", ondelete="CASCADE"), index=True
    )
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )


class DocSample(Base):
    __tablename__ = "admin_doc_sample"

    doc_sample_id: int = Column(Integer, primary_key=True, autoincrement=True)
    file_path: str = Column(String(128))
    file_name: str = Column(String(128))
    doc_titles: str = Column(String(1024), default=json.dumps([]))
    page_numbers: str = Column(String(1024), default=json.dumps([]))
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )
    doc_id: int = Column(
        Integer, ForeignKey("admin_document.doc_id", ondelete="CASCADE"), index=True
    )


class Template(Base):
    __tablename__ = "admin_template"

    template_id: int = Column(Integer, primary_key=True, autoincrement=True)
    template_code: str = Column(String(64), unique=True)
    template_name: str = Column(String(128))
    file_path: str = Column(String(128))
    file_name: str = Column(String(128))
    page_count: int = Column(Integer)
    status: int = Column(Integer, default=0, index=True)
    title_blocks = Column(CLOB, default=json.dumps([]))
    etc_blocks = Column(CLOB, default=json.dumps([]))
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )
    doc_id: int = Column(
        Integer, ForeignKey("admin_document.doc_id", ondelete="CASCADE"), index=True
    )


class TemplatePage(Base):
    __tablename__ = "admin_template_page"

    template_page_id: int = Column(Integer, primary_key=True, autoincrement=True)
    page_number: int = Column(Integer)
    page_angle: int = Column(Integer, default=0)
    page_width: int = Column(Integer)
    page_height: int = Column(Integer)
    blocks = Column(CLOB, default=json.dumps([]))
    template_id: int = Column(
        Integer,
        ForeignKey("admin_template.template_id", ondelete="CASCADE"),
        index=True,
    )


class SpellCheckDict(Base):
    __tablename__ = "admin_spell_check_dict"

    spell_dict_id: int = Column(Integer, primary_key=True, autoincrement=True)
    keyword_type: str = Column(String(16), default=KeywordType.ALL, index=True)
    wrong_keyword: str = Column(String(64))
    correct_keyword: str = Column(String(64))
    created_date: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )


class OCRNLPResult(Base):
    __tablename__ = "ocr_nlp_result"

    batch_id: str = Column(String(64), index=True)
    request_id: str = Column(String(64), primary_key=True, index=True)
    request_type: str = Column(String(10), default=ServiceType.NLP.value)
    request_from: str = Column(String(10), default=RequestFrom.AGENT.value)
    request_body = Column(CLOB, comment="OCR_NLP request body")
    request_status: str = Column(
        String(10), default=RequestStatus.Analyse_Waiting.value
    )  # 요청별 status
    nlp_file_result = Column(CLOB)  # 외부 json

    file_status: str = Column(
        String(32), default=FileStatus.WAITING.value
    )  # 파일별 status
    file_step: str = Column(String(32), default=FileStep.Upload_Waiting.value)
    nlp_status: str = Column(String(32))  # 도급계약서 유무에 따른 상태값
    req_failure_cause: str = Column(String(32))
    file_failure_cause: str = Column(String(32))

    doc_code_list = Column(CLOB, comment="NLP file doc_code list unique only")
    biz_code: str = Column(String(32), comment="biz_code")
    task_code: str = Column(String(32), comment="task_code")

    success_step: str = Column(String(32))
    file_id: str = Column(String(64), primary_key=True)
    file_name: str = Column(String(512))
    file_path: str = Column(String(2048))
    file_merged: bool = Column(Boolean, default=False)
    original_files_info: str = Column(String(2048))
    original_files_name: str = Column(String(2048))
    page_count: int = Column(Integer)
    error_message: str = Column(String(4000))

    request_date: datetime = Column(DateTime(timezone=True), default=func.now())
    analysed_date: datetime = Column(DateTime(timezone=True))
    confirmed_date: datetime = Column(DateTime(timezone=True))
    updated_date: datetime = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    user_id: int = Column(
        Integer, ForeignKey("admin_user.user_id", ondelete="SET NULL")
    )
    user_name: int = Column(
        String(32), ForeignKey("admin_user.user_name", ondelete="SET NULL")
    )


# Base.metadata.create_all(engine)
